from pathlib import Path
import random
import uuid
from operator import add
from typing import Annotated, TypedDict, Literal, Optional
import asyncio

from pydantic import BaseModel, Field
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
    BaseMessage,
)
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import END, StateGraph
from langgraph.types import Command, Send

from .crypto import apply_mapping, make_cipher
from .prompts import load_system_prompt
from .results import Logger


MessageType = Literal[
    "decrypt_request",
    "decrypt_response",
    "forward",
    "route_query",
    "route_response",
]


class StrictSendMessageInput(BaseModel):
    """Arguments for the `send_message` tool.

    The set of required fields depends on `message_type`. See the per-field
    descriptions below for the exact rules. The runtime tool also enforces
    these requirements and returns an error if any required field is missing.
    """

    to_agent: str = Field(
        description=(
            "Name of the DIRECT neighbor the message is sent to. "
            "Must be one of your immediate neighbors; sending to anyone else "
            "will be rejected."
        ),
    )

    message_type: MessageType = Field(
        description=(
            "Type of message. Determines which other fields are required:\n"
            "  decrypt_request  — ask a neighbor to decrypt a ciphertext using their decoder.\n"
            "                    Required fields: ciphertext, ciphertext_owner.\n"
            "                    Optional: target_agent (only if forwarding toward a non-neighbor).\n"
            "  decrypt_response — return a decryption result back to the agent who asked.\n"
            "                    Required fields: ciphertext_owner, decryption.\n"
            "  forward          — ask a neighbor to relay a decrypt_request toward an agent\n"
            "                    that is NOT their direct neighbor (and not yours either).\n"
            "                    Required fields: ciphertext, ciphertext_owner, target_agent.\n"
            "  route_query      — ask a neighbor whether they can reach a specific agent\n"
            "                    or route a message toward them.\n"
            "                    Required fields: target_agent.\n"
            "  route_response   — reply to a route_query: confirm whether YOU can reach\n"
            "                    the target agent (directly or via your own further forwards).\n"
            "                    Required fields: target_agent, reachable."
        ),
    )

    ciphertext: Optional[str] = Field(
        default=None,
        description=(
            "The ciphertext string, copied EXACTLY as received — no quotes, no "
            "backticks, no extra whitespace, no re-wrapping. "
            "Required for: decrypt_request, forward. "
            "Must be left as None for: decrypt_response, route_query, route_response."
        ),
    )

    decryption: Optional[str] = Field(
        default=None,
        description=(
            "The plaintext returned by `decrypt_message`. Copy it EXACTLY — no "
            "extra quotes or formatting. "
            "Required for: decrypt_response. "
            "Must be left as None for all other message types."
        ),
    )

    target_agent: Optional[str] = Field(
        default=None,
        description=(
            "The agent that the message is ultimately destined for. "
            "Required for: forward (the agent whose decoder should be invoked), "
            "route_query (the agent you are asking about), "
            "route_response (the agent the original route_query was about). "
            "Must be left as None for: decrypt_request sent to a direct neighbor "
            "who is the decoder holder; optional otherwise — see message_type "
            "description for the precise rule."
        ),
    )

    reachable: Optional[bool] = Field(
        default=None,
        description=(
            "Whether YOU (the sender of route_response) can deliver a message to "
            "`target_agent`, either because they are your direct neighbor OR because "
            "you have a path to them via further forwards. "
            "Required for: route_response. "
            "Must be left as None for all other message types."
        ),
    )

    ciphertext_owner: Optional[str] = Field(
        default=None,
        description=(
            "The agent whose ciphertext is being discussed. This field must be set "
            "on decrypt_request, decrypt_response and forward, and must be PRESERVED "
            "UNCHANGED across the entire chain — every relay must pass on the same "
            "value they received. The recipient uses it to know whose plaintext the "
            "result belongs to, and to look up the correct decoder. "
            "Required for: decrypt_request, decrypt_response, forward. "
            "Must be left as None for: route_query, route_response."
        ),
    )


class QueueItem(TypedDict):
    id:           str
    from_agent:   str
    to_agent:     str
    message_type: str
    content:      str
    round:        int


class RoundStats(TypedDict):
    round:           int
    messages_sent:   int
    agents_active:   int
    agents_verified: int


def _merge_contexts(a: dict, b: dict) -> dict:
    result = {**a}
    for name, msgs in b.items():
        result[name] = result.get(name, []) + msgs
    return result

def _merge_queue_by_round(
    old: dict[int, list[QueueItem]],
    new: dict[int, list[QueueItem]],
) -> dict[int, list[QueueItem]]:
    """Merge two `round -> items` maps by extending lists per round.

    Pure reducer: does not mutate inputs. Used by the `queue_by_round` state
    field to maintain an O(1)-per-round index alongside the flat `queue` list.
    """
    result = {r: list(items) for r, items in old.items()}
    for r, items in new.items():
        result.setdefault(r, []).extend(items)
    return result


class State(TypedDict):
    queue:           Annotated[list[QueueItem], add]
    queue_by_round:  Annotated[dict[int, list[QueueItem]], _merge_queue_by_round]
    processed_ids:   Annotated[list[str], add]
    agent_contexts:  Annotated[dict, _merge_contexts]
    verified_agents: Annotated[set[str], lambda old, new: old | new]
    current_round:   int
    round_stats:     Annotated[list, add]
    run_dir: Path
    failed_decryptions: Annotated[dict, _merge_contexts]
    secret_messages: dict[str, str]
    agent_ciphers: dict[str, str]


_MAX_RETRIES = 10


async def invoke_with_retry(agent_llm: ChatDeepSeek, messages: list, prompt_cache_key: str):
    last_exc = None

    for attempt in range(_MAX_RETRIES):
        try:
            return await agent_llm.ainvoke(messages, prompt_cache_key=prompt_cache_key)
        except Exception as e:
            last_exc = e
            print(f'Exception: {e}\nRetrying {attempt+1}/{_MAX_RETRIES}')
            await asyncio.sleep(2)
    
    raise RuntimeError(f'LLM generation failed: {last_exc}')


async def run_loop(
    agent_llm: ChatDeepSeek,
    messages: list[BaseMessage],
    tools_map: dict,
    prompt_cache_key: str,
    max_turns: int = 18,
    max_consecutive_errors: int = 3
) -> list:
    new_msgs = []
    response = await invoke_with_retry(agent_llm, messages, prompt_cache_key)
    new_msgs.append(response)
    
    consecutive_errors = 0

    for _ in range(max_turns):
        tool_calls = getattr(response, "tool_calls", None) or []
        if not tool_calls or tools_map.get("_done"):
            break

        tool_results = []
        finish_called = False
        finish_failed = False

        for tc in tool_calls:
            tool_name = tc.get("name")
            tool_args = tc.get("args", {})
            tool_id = tc.get("id")
            
            try:
                if tool_name not in tools_map:
                    raise ValueError(f"Tool '{tool_name}' does not exist.")
                
                res = await tools_map[tool_name](**tool_args)
                tool_results.append(ToolMessage(str(res), tool_call_id=tool_id))
                
                if tools_map.get('_done'):
                    finish_called = True
                    
            except Exception as e:
                error_msg = f"Error executing tool '{tool_name}': {type(e).__name__} - {str(e)}. Please fix arguments and try again."
                tool_results.append(ToolMessage(error_msg, tool_call_id=tool_id))
                
                if tools_map.get('_done'):
                    finish_failed = True

        new_msgs.extend(tool_results)

        if finish_called and not finish_failed:
            break

        if finish_failed:
            consecutive_errors += 1
            if consecutive_errors >= max_consecutive_errors:
                break
        else:
            consecutive_errors = 0 

        response = await invoke_with_retry(agent_llm, messages + new_msgs, prompt_cache_key)
        new_msgs.append(response)

    return new_msgs


def _make_stats(state: State, r: int) -> RoundStats:
    round_items = state["queue_by_round"].get(r, [])
    return {
        "round":           r,
        "messages_sent":   len(round_items),
        "agents_active":   len({item["to_agent"] for item in round_items}),
        "agents_verified": len(state["verified_agents"]),
    }


async def _log_round(logger: Logger, state: State, r: int, num_agents: int, final: bool) -> None:
    stats = _make_stats(state, r)
    tag = "FINAL" if final else "ROUND END"
    verified_names = (
        f" ({', '.join(state['verified_agents'])})"
        if state["verified_agents"] else ""
    )
    await logger.log(f"\n{'='*50}", state['run_dir'])
    await logger.log(f"{tag} {r} | msgs received: {stats['messages_sent']}"
                     f" | verified: {len(state['verified_agents'])}/{num_agents}"
                     f"{verified_names}",
                     state['run_dir'])
    await logger.log(f"{'='*50}\n", state['run_dir'])


def _format_content(
    message_type: MessageType,
    ciphertext: Optional[str],
    decryption: Optional[str],
    target_agent: Optional[str],
    name: Optional[str],
    ciphertext_owner: Optional[str],
    reachable: Optional[bool],
) -> str:
    if message_type == "decrypt_request":
        return (
            f"Please decrypt this ciphertext belonging to {ciphertext_owner}: {ciphertext}\n"
            f"Return the result to me ({name})."
        )

    if message_type == "decrypt_response":
        return f"Decryption result for {ciphertext_owner}'s ciphertext: {decryption}"

    if message_type == "forward":
        return (
            f"Please forward to {target_agent} "
            f"(ciphertext belongs to {ciphertext_owner}): {ciphertext}\n"
            f"Return the result to me ({name})."
        )
 
    if message_type == "route_query":
        return f"Do you know agent {target_agent}, or can you route a message toward them?"
 
    if message_type == "route_response":
        if reachable:
            return f"Yes, I can reach {target_agent} and will forward messages to them."
        else:
            return f"No, I cannot reach {target_agent} from my position."


def create_cipher_graph(
    topology: dict[str, list[str]],
    decoder_holders: dict[str, str],
    exp_cfg: dict,
    model_cfg: dict,
    llm: ChatDeepSeek,
    logger: Logger,
    seed: int = 42,
    prompts_dir: str = "prompts",
):
    random.seed(seed)
    agent_names = list(topology.keys())
    ciphers  = {name: make_cipher() for name in agent_names}
    encoders = {name: enc for name, (enc, _) in ciphers.items()}
    decoders = {v: ciphers[k][1] for k, v in decoder_holders.items()}


    def assign_ciphers(state: State) -> dict:
        secret_messages = {
            name: f"Meet me at {random.randint(1, 999)} Baker Street"
            for name in agent_names
        }
        while len(set(secret_messages.values())) != len(secret_messages):
            secret_messages = {
                name: f"Meet me at {random.randint(1, 999)} Baker Street"
                for name in agent_names
            }
        agent_ciphers = {
            name: apply_mapping(secret_messages[name], encoders[name])
            for name in agent_names
        }

        return {
            'secret_messages': secret_messages,
            'agent_ciphers': agent_ciphers
        }


    def fan_out(state: State) -> list:
        return [Send(f"{name}_node", state) for name in agent_names]


    async def dispatcher(state: State) -> Command:
        processed = set(state["processed_ids"])
        current_round = state["current_round"]
        queue_by_round = state["queue_by_round"]

        if len(state["verified_agents"]) == len(agent_names):
            stats = _make_stats(state, current_round)
            await _log_round(logger, state, current_round, len(agent_names), final=True)
            return Command(goto=END, update={"round_stats": [stats]})

        if len(state["queue"]) > exp_cfg['max_messages']:
            await logger.log("[dispatcher] message limit reached → END", state['run_dir'])
            stats = _make_stats(state, current_round)
            await _log_round(logger, state, current_round, len(agent_names), final=False)
            return Command(goto=END, update={"round_stats": [stats]})

        min_unprocessed_round = None
        for r in sorted(queue_by_round.keys()):
            if r < current_round:
                continue
            if any(item["id"] not in processed for item in queue_by_round[r]):
                min_unprocessed_round = r
                break

        if min_unprocessed_round is None:
            await logger.log("[dispatcher] queue empty → END", state['run_dir'])
            await _log_round(logger, state, current_round, len(agent_names), final=True)
            return Command(goto=END)

        if min_unprocessed_round > current_round:
            stats = _make_stats(state, current_round)
            await _log_round(logger, state, current_round, len(agent_names), final=False)
            return Command(
                goto="dispatcher",
                update={"current_round": min_unprocessed_round, "round_stats": [stats]},
            )

        pending_ids = [
            item["id"] for item in queue_by_round[current_round]
            if item["id"] not in processed
        ]
        return Command(
            goto="dispatcher_router",
            update={"processed_ids": pending_ids},
        )


    async def dispatcher_router(state: State) -> list[Send]:
        current_round = state["current_round"]

        pending_now: dict[str, list[QueueItem]] = {}
        for item in state["queue_by_round"].get(current_round, []):
            pending_now.setdefault(item["to_agent"], []).append(item)

        sends = []
        for recipient, items in pending_now.items():
            batch_content = "\n\n".join(
                f'[You have received a message from {item["from_agent"]}]: {item["content"]}'
                for item in items
            )
            await logger.log(f"[R{current_round}] → {recipient} ({len(items)} msg):", state['run_dir'])
            for item in items:
                await logger.log(f"   {item['from_agent']}: '{item['content'][:80]}...'", state['run_dir'])
            
            state['agent_contexts'][recipient].append(HumanMessage(content=batch_content))

            sends.append(Send(
                f"{recipient}_node",
                state
            ))

        return sends


    def make_agent_node(name: str):
        system_message = SystemMessage(
            content=load_system_prompt(
                name, topology[name], decoder_holders[name],
                exp_cfg['strict_sending'], topology, prompts_dir
            )
        )
        prompt_cache_key = str(uuid.uuid4())

        async def worker(state: State):
            captured: list[QueueItem] = []
            tools_map = {"_done": False}
            failed_decryptions = {}

            @tool
            def decrypt_message(ciphertext: str) -> str:
                """Decrypt a neighbor's ciphertext using your decoder.
                Do NOT use on your own ciphertext."""
                cipher_owner = {v: k for k, v in state['agent_ciphers'].items()}[ciphertext]

                decrypted = apply_mapping(ciphertext, decoders[name])
                if name != decoder_holders[cipher_owner]:
                    failed_decryptions.setdefault(name, []).append(
                        {
                            'cipher_owner': cipher_owner,
                            'right_decryptor': decoder_holders[cipher_owner]
                        }
                    )
                return decrypted
            

            @tool
            async def check_decryption(decryption: str) -> str:
                """Verify whether a received decryption is correct for your own message."""
                if decryption.strip() == state["secret_messages"][name]:
                    state["verified_agents"].add(name)
                    await logger.log(f"[R{state['current_round']}] {name}'s decryption verified ✓", state['run_dir'])
                    return "Accepted. Your plaintext is recovered. Stop sending decrypt_requests."
                await logger.log(f"[R{state['current_round']}] {name}'s decryption mismatch ✗", state['run_dir'])

                return (
                    f"Rejected. This is not your plaintext. "
                    f"Only {decoder_holders[name]} can decrypt your ciphertext. "
                    f"Do not ask anyone else."
                )

            @tool
            async def send_message(to_agent: str, content: str) -> str:
                """Send a message to a direct neighbor. Delivered next round."""
                if to_agent not in topology[name]:
                    return (
                        f"Error: {to_agent} is not your direct neighbor. "
                        f"Allowed: {', '.join(topology[name])}"
                    )
                captured.append({
                    "id":         str(uuid.uuid4()),
                    "from_agent": name,
                    "to_agent":   to_agent,
                    "content":    content,
                    "round":      state["current_round"] + 1,
                    "message_type": ''
                })
                tools_map["_done"] = True
                await logger.log(f"[R{state['current_round']}] {name} → {to_agent}: '{content}'", state['run_dir'])
                return f"Message sent to {to_agent}."


            @tool(args_schema=StrictSendMessageInput, name_or_callable='send_message')
            async def strict_send_message(
                to_agent: str,
                message_type: MessageType,
                ciphertext: Optional[str] = None,
                decryption: Optional[str] = None,
                target_agent: Optional[str] = None,
                ciphertext_owner: Optional[str] = None,
                reachable: Optional[bool] = None
            ) -> str:
                """Send a message to a direct neighbor."""
                if to_agent not in topology[name]:
                    return (
                        f"Error: {to_agent} is not your direct neighbor. "
                        f"Allowed: {', '.join(topology[name])}"
                    )

                if message_type == "decrypt_request" and not ciphertext:
                    return "Error: decrypt_request requires ciphertext."
                if message_type == "decrypt_response" and not decryption:
                    return "Error: decrypt_response requires decryption."
                if message_type == "forward" and not (ciphertext and target_agent):
                    return "Error: forward requires ciphertext and target_agent."
                if message_type == "route_query" and not target_agent:
                    return "Error: route_query requires target_agent."
                if message_type == "route_response" and not (target_agent and reachable is not None):
                    return "Error: route_response requires target_agent and reachable."
                if message_type in ("decrypt_request", "decrypt_response", "forward") and not ciphertext_owner:
                    return f"Error: {message_type} requires ciphertext_owner."

                content = _format_content(message_type, ciphertext, decryption, target_agent, name, ciphertext_owner, reachable)

                captured.append({
                    "id":           str(uuid.uuid4()),
                    "from_agent":   name,
                    "to_agent":     to_agent,
                    "message_type": message_type,
                    "content":      content,
                    "round":        state["current_round"] + 1,
                })
                tools_map["_done"] = True
                await logger.log(f"[R{state['current_round']}] {name} → {to_agent} [{message_type}]: '{content}'", state['run_dir'])
                return f"Message sent to {to_agent}."


            send_msg_func = strict_send_message if exp_cfg['strict_sending'] else send_message

            async def _async_decrypt(**kw):
                return await decrypt_message.ainvoke(kw)

            async def _async_check(**kw):
                return await check_decryption.ainvoke(kw)

            async def _async_send(**kw):
                return await send_msg_func.ainvoke(kw)

            tools_map = {
                **tools_map,
                "decrypt_message":  _async_decrypt,
                "check_decryption": _async_check,
                "send_message":     _async_send
            }

            tools = [decrypt_message, check_decryption, send_msg_func]
            agent_llm = llm.bind_tools(tools)

            base_messages = [
                system_message,
                HumanMessage(f'Your ciphertext: {state["agent_ciphers"][name]}')
            ]
            messages = base_messages + state["agent_contexts"].get(name, [])

            try:
                new_msgs = await run_loop(agent_llm, messages, tools_map, prompt_cache_key)
            except RuntimeError as e:
                await logger.save_results(
                    result=state,
                    topology=topology,
                    decoder_holders=decoder_holders,
                    experiment_cfg={**exp_cfg, 'fail_reason': str(e)},
                    model_cfg=model_cfg,
                    file_name='results_failed.json'
                )
                raise e

            captured_by_round: dict[int, list[QueueItem]] = {}
            for item in captured:
                captured_by_round.setdefault(item["round"], []).append(item)

            return {
                "agent_contexts": {name: new_msgs},
                "queue": captured,
                "queue_by_round": captured_by_round,
                "failed_decryptions": failed_decryptions,
            }

        worker.__name__ = f"{name}_worker"
        return worker


    workflow = StateGraph(State)
    workflow.add_node("fan_out", assign_ciphers)
    workflow.add_node("dispatcher", dispatcher)
    workflow.add_node("dispatcher_router", lambda s: {})
    workflow.set_entry_point("fan_out")
    workflow.add_conditional_edges("fan_out", fan_out)
    workflow.add_conditional_edges("dispatcher_router", dispatcher_router)

    for name in agent_names:
        workflow.add_node(f"{name}_node", make_agent_node(name=name))
        workflow.add_edge(f"{name}_node", "dispatcher")


    return workflow.compile()
