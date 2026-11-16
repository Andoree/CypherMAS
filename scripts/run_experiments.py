import argparse
import sys
import multiprocessing
from pathlib import Path
import yaml
import asyncio
import os
import gc

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from codebooks import assign_decoders, create_cipher_graph, make_topology
from codebooks.results import Logger, create_run_dir


load_dotenv()


def load_yaml(path: str) -> dict:
    return yaml.safe_load(Path(path).read_text())


def build_llm(cfg: dict) -> ChatDeepSeek:
    return ChatDeepSeek(
        model=cfg["model"],
        base_url=os.getenv(cfg["api_base"]),
        api_key=os.getenv(cfg["api_key"]),
        temperature=cfg.get("temperature", 1.0),
        top_p=cfg.get("top_p", 0.95),
        max_tokens=cfg.get("max_tokens", 8192),
        extra_body=cfg.get("extra_body", {}),
        seed=cfg.get('seed', 42),
        use_responses_api=cfg.get('use_responses_api', False),
        timeout=1200.0
    )


async def main(args):
    exp_cfg, results_root = args
    res_dir_template = '{topology}_{num_agents}'
    res_dir = res_dir_template.format(
        topology=exp_cfg['topology_type'],
        num_agents=exp_cfg['num_agents'],
    )
    model_cfg = load_yaml("configs/models.yaml")[exp_cfg['model']]

    if exp_cfg["custom_topology_file"]:
        topology = load_yaml(exp_cfg["custom_topology_file"])
    else:
        topology = make_topology(exp_cfg["num_agents"], exp_cfg["topology_type"])

    decoder_holders = assign_decoders(topology, mode=exp_cfg.get("decoder_mode", "max"))

    logger = Logger(
        verbose=exp_cfg.get('verbose', True),
    )

    llm = build_llm(model_cfg)

    app = create_cipher_graph(
        topology=topology,
        decoder_holders=decoder_holders,
        exp_cfg=exp_cfg,
        model_cfg=model_cfg,
        llm=llm,
        logger=logger,
    )

    async def _one(i):
        try:
            result = await app.ainvoke(
                {
                    "queue":           [],
                    "processed_ids":   [],
                    "agent_contexts":  {},
                    "verified_agents": set(),
                    "current_round":   0,
                    "round_stats":     [],
                    "run_dir": create_run_dir(
                        exp_cfg['model'],
                        res_dir,
                        exp_cfg['strict_sending'],
                        results_root
                    ) / f'run_{i:>02}',
                    "secret_messages": {},
                    "agent_ciphers": {}
                }
            )

            await logger.log_summary(result, topology)
            await logger.save_results(
                result=result,
                topology=topology,
                decoder_holders=decoder_holders,
                experiment_cfg=exp_cfg,
                model_cfg=model_cfg,
            )
        except Exception as e:
            print(f"Error in the process {os.getpid()}: {e}")

    run_dir = create_run_dir(
        exp_cfg['model'],
        res_dir,
        exp_cfg['strict_sending'],
        results_root
    )
    done_runs = set()
    for dirpath, _, files in run_dir.walk():
        if 'results.json' in files:
            done_runs.add(str(dirpath.name))

    tasks = []
    if len(done_runs) < exp_cfg['num_runs']:
        i = 0
        while len(tasks) < (exp_cfg['num_runs'] - len(done_runs)):
            i += 1
            run_name = f'run_{i:>02}'
            if run_name in done_runs:
                continue
            
            (run_dir / run_name).mkdir(parents=True, exist_ok=True)
            (run_dir / run_name / 'execution_log.md').write_text('')
            tasks.append(_one(i))

    await asyncio.gather(*tasks)

    del app, llm
    gc.collect()

    await asyncio.sleep(0.1)


def run(args):
    return asyncio.run(main(args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', '-c', type=str, required=True)
    parser.add_argument('--max-workers', type=int, default=None)
    parser.add_argument('--results-root', '-r', type=str, default='results')
    args = parser.parse_args()

    exp_cfg = load_yaml(args.config)

    pool_args = []
    topologies = exp_cfg['topologies']

    for topology in topologies:
        for n in exp_cfg['num_agents_list']:
            cfg = {
                'model': exp_cfg['model'],
                'topology_type': topology,
                'num_agents': n,
                'custom_topology_file': None,
                'decoder_mode': exp_cfg['decoder_mode'],
                'max_messages': exp_cfg['max_messages'],
                'num_runs': exp_cfg['num_runs'],
                'strict_sending': exp_cfg.get('strict_sending', False),
                'verbose': False
            }

            pool_args.append((cfg, args.results_root))

    pbar = tqdm(
        total=len(pool_args),
        leave=True,
    )

    with multiprocessing.Pool(processes=args.max_workers) as pool:
        for _ in pool.imap_unordered(run, pool_args, chunksize=1):
            pbar.update(1)
