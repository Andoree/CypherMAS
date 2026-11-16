from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Any, Optional


def bfs_distances(topology: dict[str, list[str]], source: str) -> dict[str, int]:
    dist = {source: 0}
    q = [source]
    while q:
        node = q.pop(0)
        for nb in topology.get(node, []):
            if nb not in dist:
                dist[nb] = dist[node] + 1
                q.append(nb)
    return dist


def all_pairs_distances(topology: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    return {n: bfs_distances(topology, n) for n in topology}


def _parse_args(raw) -> dict:
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    return raw if isinstance(raw, dict) else {}


def extract_tool_events(agent_contexts: dict[str, list[dict]]) -> dict[str, list[dict]]:
    events: dict[str, list[dict]] = defaultdict(list)
    for agent, msgs in agent_contexts.items():
        for i, msg in enumerate(msgs):
            if msg.get("type") != "ai":
                continue
            tcs = msg.get("tool_calls") or []
            if not tcs:
                continue
            results: list[Optional[str]] = []
            j = i + 1
            while j < len(msgs) and msgs[j].get("type") == "tool":
                results.append(msgs[j].get("content"))
                j += 1
            for k, tc in enumerate(tcs):
                events[agent].append({
                    "name":       tc.get("name"),
                    "args":       _parse_args(tc.get("args")),
                    "result":     results[k] if k < len(results) else None,
                    "msg_index":  i,
                })

    return events


def is_error_result(text: Optional[str]) -> bool:
    if not text:
        return False
    t = text.strip().lower()
    return t.startswith("error") or t.startswith("rejected")


def build_enriched_queue(results: dict) -> tuple[list[dict], dict[str, list[dict]], list[dict]]:
    queue = results.get("queue", [])
    events = extract_tool_events(results.get("agent_contexts", {}))

    valid_sends: dict[str, list[dict]] = defaultdict(list)
    rejected_sends: list[dict] = []
    for agent, ev_list in events.items():
        for ev in ev_list:
            if ev["name"] != "send_message":
                continue
            if is_error_result(ev["result"]):
                rejected_sends.append({"agent": agent, **ev})
            else:
                valid_sends[agent].append(ev)

    ptr: dict[str, int] = defaultdict(int)
    enriched: list[dict] = []
    for qi, qmsg in enumerate(queue):
        agent = qmsg.get("from_agent")
        idx = ptr[agent]
        ev = valid_sends[agent][idx] if idx < len(valid_sends[agent]) else None
        ptr[agent] += 1
        entry = dict(qmsg)
        entry["_qi"] = qi
        entry["_args"] = ev["args"] if ev else {}
        enriched.append(entry)

    return enriched, events, rejected_sends


def compute_run_metrics(results: dict, detail: bool = False) -> dict:
    topology        = results.get("topology", {})
    decoder_holders = results.get("decoder_holders", {})
    agent_ciphers   = results.get("agent_ciphers", {})
    summary         = results.get("summary", {})
    failed_decryptions = results.get("failed_decryptions", {}) or {}
    experiment      = results.get("experiment", {})

    dist = all_pairs_distances(topology)
    cipher_to_owner = {v: k for k, v in agent_ciphers.items()}

    enriched, events, rejected_sends = build_enriched_queue(results)
    total_messages = len(enriched)

    invalid_send_count = len(rejected_sends)
    invalid_send_examples = [
        {"agent": r["agent"], "attempted_to": r["args"].get("to_agent"), "error": r["result"]}
        for r in rejected_sends
    ]

    wrong_decryptor_count = sum(len(v) for v in failed_decryptions.values())
    wrong_decryptor_examples = [
        {"agent": agent, "cipher_owner": item["cipher_owner"], "right_decryptor": item["right_decryptor"]}
        for agent, items in failed_decryptions.items() for item in items
    ]

    failed_verification_count = 0
    failed_verification_examples = []
    for agent, ev_list in events.items():
        for ev in ev_list:
            if ev["name"] == "check_decryption" and is_error_result(ev["result"]):
                failed_verification_count += 1
                if len(failed_verification_examples) < 5:
                    failed_verification_examples.append({"agent": agent, "result": ev["result"]})

    decrypt_calls = []
    for agent, ev_list in events.items():
        for ev in ev_list:
            if ev["name"] == "decrypt_message":
                decrypt_calls.append({
                    "agent": agent,
                    "ciphertext": ev["args"].get("ciphertext"),
                    "result": ev["result"],
                    "msg_index": ev["msg_index"],
                })
    total_decrypt_attempts = len(decrypt_calls)

    sent_by_agent: dict[str, list[str]] = defaultdict(list)
    for e in enriched:
        sent_by_agent[e["from_agent"]].append(e.get("content") or "")

    decrypt_without_followup = 0
    for dc in decrypt_calls:
        result = dc["result"]
        if not result:
            continue
        followed = any(result in content for content in sent_by_agent.get(dc["agent"], []))
        if not followed:
            decrypt_without_followup += 1

    sent_ciphers_by_agent: dict[str, set[str]] = defaultdict(set)
    decrypted_ciphers_by_agent: dict[str, set[str]] = defaultdict(set)

    for e in enriched:
        cipher = e["_args"].get("ciphertext")
        if not cipher:
            content = e.get("content") or ""
            for o, c in agent_ciphers.items():
                if c and c in content:
                    cipher = c
                    break
        if cipher:
            sent_ciphers_by_agent[e["from_agent"]].add(cipher)

    for agent, ev_list in events.items():
        for ev in ev_list:
            if ev["name"] == "decrypt_message":
                ct = ev["args"].get("ciphertext")
                if ct:
                    decrypted_ciphers_by_agent[agent].add(ct)

    dropped_request_count = 0
    total_requests = 0
    dropped_request_examples = []
    
    for e in enriched:
        mtype = e.get("message_type")
        if mtype not in ("forward", "decrypt_request"):
            continue
            
        receiver = e["to_agent"]
        cipher = e["_args"].get("ciphertext")
        if not cipher:
            content = e.get("content") or ""
            for o, c in agent_ciphers.items():
                if c and c in content:
                    cipher = c
                    break
                    
        if not cipher:
            continue
            
        total_requests += 1
        
        forwarded = cipher in sent_ciphers_by_agent.get(receiver, set())
        decrypted = cipher in decrypted_ciphers_by_agent.get(receiver, set())
        
        if not forwarded and not decrypted:
            dropped_request_count += 1
            if len(dropped_request_examples) < 5:
                dropped_request_examples.append({
                    "agent": receiver,
                    "from_agent": e["from_agent"],
                    "round": e.get("round"),
                    "mtype": mtype
                })
                
    wrong_direction_count = 0
    wrong_direction_total = 0
    wrong_return_direction_count = 0
    wrong_return_direction_total = 0
    
    plaintext_to_owner = {}
    for agent, ev_list in events.items():
        for ev in ev_list:
            if ev["name"] == "decrypt_message" and ev["result"]:
                ct = ev["args"].get("ciphertext")
                if ct in cipher_to_owner:
                    plaintext_to_owner[ev["result"]] = cipher_to_owner[ct]

    for e in enriched:
        args = e["_args"]
        mtype = e.get("message_type")
        content = e.get("content") or ""
        
        cipher = args.get("ciphertext")
        plaintext = args.get("decryption") or args.get("plaintext")
        
        owner = None
        is_response = False
        
        if cipher:
            owner = cipher_to_owner.get(cipher)
        elif plaintext:
            owner = plaintext_to_owner.get(plaintext)
            is_response = True
            
        if owner is None:
            for o, c in agent_ciphers.items():
                if c and c in content:
                    owner = o
                    break
            
            if owner is None:
                for p, o in plaintext_to_owner.items():
                    if p and p in content:
                        owner = o
                        is_response = True
                        break

        if mtype == "decrypt_response":
            is_response = True
        elif mtype in ("forward", "decrypt_request") and owner is not None:
            is_response = False

        if owner is None or owner not in decoder_holders:
            continue
            
        target = owner if is_response else decoder_holders[owner]
        
        d_from = dist.get(e["from_agent"], {}).get(target)
        d_to = dist.get(e["to_agent"], {}).get(target)
        
        if d_from is None or d_to is None:
            continue
            
        if is_response:
            wrong_return_direction_total += 1
            if d_to > d_from:
                wrong_return_direction_count += 1
        else:
            wrong_direction_total += 1
            if d_to > d_from:
                wrong_direction_count += 1

    cipher_corrupted_count = 0
    cipher_checked_total = 0
    for e in enriched:
        args = e["_args"]
        owner = args.get("ciphertext_owner")
        actual = args.get("ciphertext")
        if actual:
            cipher_checked_total += 1
            if actual not in set(agent_ciphers.values()):
                cipher_corrupted_count += 1

    seen: dict[tuple, int] = defaultdict(int)
    for e in enriched:
        key = (e["from_agent"], e["to_agent"], e.get("message_type"), e.get("content"))
        seen[key] += 1
    duplicate_messages = sum(c - 1 for c in seen.values() if c > 1)

    plaintext_to_owner = {}
    for agent, ev_list in events.items():
        for ev in ev_list:
            if ev["name"] == "decrypt_message" and ev["result"]:
                ct = ev["args"].get("ciphertext")
                if ct in cipher_to_owner:
                    plaintext_to_owner[ev["result"]] = cipher_to_owner[ct]

    cipher_lifecycle = {
        owner: {
            "initiated": False,
            "reached_decoder": False,
            "returning": False,
            "returned_to_owner": False
        }
        for owner in agent_ciphers if owner in decoder_holders
    }

    for e in enriched:
        args = e["_args"]
        content = e.get("content") or ""
        cipher = args.get("ciphertext")
        plaintext = args.get("decryption") or args.get("plaintext")
        
        owner = None
        is_response = False
        
        if cipher:
            owner = cipher_to_owner.get(cipher)
        elif plaintext:
            owner = plaintext_to_owner.get(plaintext)
            is_response = True
            
        if owner is None:
            for o, c in agent_ciphers.items():
                if c and c in content:
                    owner = o
                    break
            if owner is None:
                for p, o in plaintext_to_owner.items():
                    if p and p in content:
                        owner = o
                        is_response = True
                        break

        if owner is None or owner not in cipher_lifecycle:
            continue
            
        holder = decoder_holders[owner]
        
        if not is_response:
            if e["from_agent"] == owner:
                cipher_lifecycle[owner]["initiated"] = True
            if e["to_agent"] == holder:
                cipher_lifecycle[owner]["reached_decoder"] = True
        else:
            if e["from_agent"] == holder:
                cipher_lifecycle[owner]["returning"] = True
            if e["to_agent"] == owner:
                cipher_lifecycle[owner]["returned_to_owner"] = True

    completed = summary.get("agents_verified", 0)
    total_ciphers = len(topology)
    
    bottlenecks = {
        "completed": completed,
        "stuck_at_owner_init": 0,
        "stuck_in_transit_to_decoder": 0,
        "stuck_at_decoder_processing": 0,
        "stuck_in_transit_to_owner": 0,
        "stuck_at_owner_verification": 0,
    }
    
    reached_owner_count = sum(1 for life in cipher_lifecycle.values() if life["returned_to_owner"])
    bottlenecks["stuck_at_owner_verification"] = max(0, reached_owner_count - completed)
    
    for owner, life in cipher_lifecycle.items():
        if life["returned_to_owner"]:
            continue
            
        if not life["initiated"]:
            bottlenecks["stuck_at_owner_init"] += 1
        elif not life["reached_decoder"]:
            bottlenecks["stuck_in_transit_to_decoder"] += 1
        elif not life["returning"]:
            bottlenecks["stuck_at_decoder_processing"] += 1
        elif not life["returned_to_owner"]:
            bottlenecks["stuck_in_transit_to_owner"] += 1

    num_agents = summary.get("agents_total", len(topology)) or len(topology)
    success_rate = (summary.get("agents_verified", 0) / num_agents) if num_agents else 0.0

    out = {
        "mode": "strict" if experiment.get("strict_sending") else "free_text",
        "model": experiment.get("model") or results.get("model"),
        "topology_type": experiment.get("topology_type"),
        "num_agents": num_agents,
        "rounds_elapsed": summary.get("rounds_elapsed", 0),
        "total_messages": total_messages,
        "agents_verified": summary.get("agents_verified", 0),
        "success_rate": success_rate,
        "total_decrypt_attempts": total_decrypt_attempts,
        "errors": {
            "invalid_send":          invalid_send_count,
            "wrong_decryptor":       wrong_decryptor_count,
            "failed_verification":   failed_verification_count,
            "decrypt_without_followup": decrypt_without_followup,
            "wrong_direction":       wrong_direction_count,
            "wrong_return_direction": wrong_return_direction_count,
            "total_wrong_direction": wrong_direction_count + wrong_return_direction_count,
            "dropped_request":       dropped_request_count,
            "cipher_corrupted":      cipher_corrupted_count,
            "duplicate_messages":    duplicate_messages,
        },
        "denominators": {
            "invalid_send":          total_messages + invalid_send_count,
            "wrong_decryptor":       total_decrypt_attempts,
            "failed_verification":   None,
            "decrypt_without_followup": total_decrypt_attempts,
            "wrong_direction":       wrong_direction_total,
            "wrong_return_direction": wrong_return_direction_total,
            "total_wrong_direction": total_messages,
            "dropped_request":       total_messages,
            "cipher_corrupted":      cipher_checked_total,
            "duplicate_messages":    total_messages,
        },
        "examples": {
            "invalid_send":    invalid_send_examples,
            "wrong_decryptor": wrong_decryptor_examples,
            "failed_verification": failed_verification_examples,
            "dropped_request": dropped_request_examples,
        },
        "bottlenecks": bottlenecks,
        "total_ciphers": total_ciphers
    }

    if detail:
        out["_enriched_queue"] = enriched

    return out


ERROR_LABELS = [
    ("invalid_send",             "Invalid send (to none neighbor)"),
    ("wrong_decryptor",          "Failed Decryptions"),
    ("failed_verification",      "Decryption Rejected"),
    ("decrypt_without_followup", "Decrypted without Followup"),
    ("wrong_direction",          "Cipher Wrong Direction"),
    ("wrong_return_direction",   "Decryption Wrong Direction"),
    ("dropped_request",          "Dropped Request"),
    ("cipher_corrupted",         "Corrupted Ciphertext"),
    ("duplicate_messages",       "Duplicate Messages"),
    ("total_wrong_direction",    "Total Wrong Direction")
]

def _ratio_str(count: int, denom: Optional[int]) -> str:
    if denom is None:
        return f"{count:>6d}"
    if denom == 0:
        return f"{count:>6d}   ( n/a )"
    return f"{count:>6d}   ({count/denom:6.1%} of {denom})"

def print_bottlenecks_report(m: dict) -> None:
    b = m.get("bottlenecks", {})
    total = m.get("total_ciphers", 0)
    if total == 0:
        return
        
    def fmt_bottleneck(val):
        if total == 0:
            return f"{val:>6d}"
        return f"{val:>6d}   ({val/total:.3f} of {total})"

    print(f"\n  Agent-Level Errors:")
    print(f"  {'-'*84}")
    print(f"  {'Completed':<55}{fmt_bottleneck(b.get('completed', 0))}")
    print(f"  {'Initial Fail':<55}{fmt_bottleneck(b.get('stuck_at_owner_init', 0))}")
    print(f"  {'Transition to Decoder Fail':<55}{fmt_bottleneck(b.get('stuck_in_transit_to_decoder', 0))}")
    print(f"  {'Decoder Stuck':<55}{fmt_bottleneck(b.get('stuck_at_decoder_processing', 0))}")
    print(f"  {'Transition to Owner Fail':<55}{fmt_bottleneck(b.get('stuck_in_transit_to_owner', 0))}")
    print(f"  {'Verify Stuck':<55}{fmt_bottleneck(b.get('stuck_at_owner_verification', 0))}")


def print_run_report(name: str, m: dict) -> None:
    print(f"\n{'='*88}")
    print(f"RUN: {name}   [mode={m['mode']}  model={m['model']}  topology={m['topology_type']}"
          f"  n_agents={m['num_agents']}]")
    print(f"{'='*88}")
    print(f"  Rounds elapsed: {m['rounds_elapsed']:<6}  Total messages: {m['total_messages']:<6}"
          f"  Decrypt attempts: {m['total_decrypt_attempts']}")
    print(f"  Agents verified: {m['agents_verified']}/{m['num_agents']}"
          f"   ({m['success_rate']:.1%} success)")
    print()
    print(f"  {'Error category':<55}{'Count (ratio)'}")
    print(f"  {'-'*84}")
    errs = m["errors"]
    denoms = m["denominators"]
    for key, label in ERROR_LABELS:
        print(f"  {label:<55}{_ratio_str(errs[key], denoms[key])}")

    ex = m["examples"]
    if ex["invalid_send"]:
        print("\n  invalid_send examples:")
        for e in ex["invalid_send"][:5]:
            print(f"    - {e['agent']} -> {e['attempted_to']}: {e['error']}")
    if ex["wrong_decryptor"]:
        print("\n  wrong_decryptor examples:")
        for e in ex["wrong_decryptor"][:5]:
            print(f"    - {e['agent']} decrypted ciphertext of {e['cipher_owner']}"
                  f" (Right decryptor is {e['right_decryptor']})")
    if ex["failed_verification"]:
        print("\n  failed_verification examples:")
        for e in ex["failed_verification"][:5]:
            print(f"    - {e['agent']}: {e['result']}")
    if ex["dropped_request"]:
        print("\n  dropped_request examples:")
        for e in ex["dropped_request"][:5]:
            print(f"    - {e['agent']} got {e['mtype']} from {e['from_agent']} in round {e['round']} and ignored it")
    print_bottlenecks_report(m)


def print_message_detail(m: dict) -> None:
    enriched = m.get("_enriched_queue", [])
    if not enriched:
        return
    print("\n  Queue analysis:")
    print(f"  {'#':<4}{'Rnd':<5}{'From':<8}{'->':<3}{'To':<8}{'Type':<18}{'Content'}")
    print(f"  {'-'*100}")
    for i, e in enumerate(enriched, 1):
        content = (e.get("content") or "").replace("\n", " ")
        if len(content) > 60:
            content = content[:57] + "..."
        print(f"  {i:<4}{e.get('round', ''):<5}{e['from_agent']:<8}{'->':<3}"
              f"{e['to_agent']:<8}{(e.get('message_type') or ''):<18}{content}")


def aggregate(runs: list[dict]) -> dict:
    def stat(vals):
        vals = [v for v in vals if v is not None]
        if not vals:
            return None
        return {"mean": mean(vals), "stdev": stdev(vals) if len(vals) > 1 else 0.0,
                "min": min(vals), "max": max(vals)}

    ratios_per_key: dict[str, list[Optional[float]]] = {key: [] for key, _ in ERROR_LABELS}
    for r in runs:
        errs = r["errors"]
        denoms = r["denominators"]
        for key, _ in ERROR_LABELS:
            d = denoms.get(key)
            c = errs.get(key)
            if d is None or d == 0 or c is None:
                ratios_per_key[key].append(None)
            else:
                ratios_per_key[key].append(c / d)

    agg: dict[str, Any] = {
        "num_runs": len(runs),
        "success_rate": stat([r["success_rate"] for r in runs]),
        "rounds_elapsed": stat([r["rounds_elapsed"] for r in runs]),
        "total_messages": stat([r["total_messages"] for r in runs]),
        "errors": {},
        "ratios": {},
    }
    for key, _label in ERROR_LABELS:
        agg["errors"][key] = stat([r["errors"][key] for r in runs])
        agg["ratios"][key] = stat(ratios_per_key[key])
    
    b_keys = [
        "completed", 
        "stuck_at_owner_init", 
        "stuck_in_transit_to_decoder", 
        "stuck_at_decoder_processing", 
        "stuck_in_transit_to_owner",
        "stuck_at_owner_verification"
    ]
    agg["bottlenecks"] = {}
    for k in b_keys:
        agg["bottlenecks"][k] = stat([r["bottlenecks"][k] for r in runs])

    agg["bottlenecks_ratios"] = {}
    for k in b_keys:
        run_ratios = []
        for r in runs:
            total_c = r.get("total_ciphers", 0)
            if total_c > 0:
                run_ratios.append(r["bottlenecks"][k] / total_c)
        agg["bottlenecks_ratios"][k] = stat(run_ratios)

    return agg


def print_aggregate_report(agg: dict) -> None:
    print(f"  ({agg['num_runs']} runs)")

    def fmt(v):
        if v is None:
            return "N/A"
        return f"mean={v['mean']:.3f}  stdev={v['stdev']:.3f}  min={v['min']:.3f}  max={v['max']:.3f}"

    def fmt_ratio(v):
        if v is None:
            return "N/A"
        return (f"mean={v['mean']:.2f}  stdev={v['stdev']:.2f}  "
                f"min={v['min']:.2f}  max={v['max']:.2f}")

    print(f"  {'success_rate':<25}{fmt(agg['success_rate'])}")
    print(f"  {'rounds_elapsed':<25}{fmt(agg['rounds_elapsed'])}")
    print(f"  {'total_messages':<25}{fmt(agg['total_messages'])}")
    print()
    print(f"  {'Error category':<55}{'Counts: mean / stdev / min / max'}")
    print(f"  {'-'*95}")
    for key, label in ERROR_LABELS:
        print(f"  {label:<55}{fmt(agg['errors'][key])}")

    print()
    print(f"  {'Error category':<55}{'Ratios: mean / stdev / min / max'}")
    print(f"  {'-'*95}")
    for key, label in ERROR_LABELS:
        print(f"  {label:<55}{fmt_ratio(agg['ratios'][key])}")

    print()
    print(f"  {'Bottlenecks Ratios (mean / stdev / min / max)':<55}")
    print(f"  {'-'*95}")
    
    b_labels = [
        ("completed", "Completed"),
        ("stuck_at_owner_init", "Initial Fail"),
        ("stuck_in_transit_to_decoder", "Transition to Decoder Fail"),
        ("stuck_in_transit_to_owner", "Transition to Owner Fail"),
        ("stuck_at_decoder_processing", "Decoder Stuck"),
        ("stuck_at_owner_verification", "Verify Stuck"),
    ]
    
    for key, label in b_labels:
        v = agg["bottlenecks_ratios"][key]
        if v is None:
            val_str = "N/A"
        else:
            val_str = f"mean={v['mean']:.3f}  stdev={v['stdev']:.3f}  min={v['min']:.3f}  max={v['max']:.3f}"
        print(f"  {label:<55}{val_str}")


models = {
    'qwen3.5-4b': 'Qwen3.5-4B',
    'qwen3.5-9b': 'Qwen3.5-9B',
    'qwen3.6-27b': 'Qwen3.6-27B',
    'qwen3.6-35b': 'Qwen3.6-35B-A3B',
    'gemma4-31b': 'Gemma4-31B',
    'devstral-24b': 'Devstral-Small-2-24B',
    'gpt-oss-20b': 'gpt-oss-20b',
    'gpt-oss-120b': 'gpt-oss-120b',
    'glm-5.2': 'GLM-5.2'
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-dir', '-r', type=str, default='results')
    parser.add_argument('--model', '-m', type=str)
    parser.add_argument('--graph-size', '-gs', type=int)
    parser.add_argument('--topology', '-t', type=str)
    parser.add_argument('--num-runs', type=int, default=3)
    parser.add_argument('--strict', action='store_true')
    parser.add_argument('--detail', action='store_true')
    parser.add_argument('--per-run', action='store_true')
    args = parser.parse_args()

    mode = 'strict' if args.strict else 'free_text'

    directory = Path(args.root_dir) / mode / f'{args.topology}_{args.graph_size}' / args.model

    paths = []
    paths.extend(sorted(Path(directory).glob("**/results.json")))
    paths = paths[:args.num_runs]

    metrics: list[dict] = []
    for p in paths:
        try:
            with open(p, encoding="utf-8") as fp:
                results = json.load(fp)
        except Exception as e:
            print(f"[warn] failed to read {p}: {e}")
            continue
        m = compute_run_metrics(results, detail=args.detail)
        metrics.append(m)
        if args.per_run:
            print_run_report(str(p), m)
            if args.detail:
                print_message_detail(m)

    agg = aggregate(metrics)
    print(' ', '#'*80)
    print(' ', models[args.model], args.topology.title(), f'N={args.graph_size}')
    print(' ', '#'*80)
    print_aggregate_report(agg)
