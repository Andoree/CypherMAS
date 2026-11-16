import json
from pathlib import Path

import aiofiles


class Logger:
    def __init__(
        self,
        verbose: bool = True,
    ):
        self.verbose = verbose

    async def log(self, text: str, run_dir: Path | None) -> None:
        if self.verbose:
            print(text)
            
        if run_dir is not None:
            file_path = run_dir / 'execution_log.md'
            async with aiofiles.open(file_path, "a", encoding="utf-8") as f:
                await f.write(text + "\n")


    async def save_results(
        self,
        result: dict,
        topology: dict,
        decoder_holders: dict,
        experiment_cfg: dict,
        model_cfg: dict,
        file_name: str = 'results.json'
    ) -> None:
        """Save experiment results to a JSON file."""
        if result['run_dir'] is None:
            return
        
        clean_model_cfg = dict(model_cfg)
        clean_model_cfg.pop('api_base', None)
        clean_model_cfg.pop('api_key', None)

        payload = {
            "experiment":      experiment_cfg,
            "model":           clean_model_cfg,
            "topology":        topology,
            "decoder_holders": decoder_holders,
            "summary": {
                "agents_total":    len(topology),
                "agents_verified": len(result["verified_agents"]),
                "total_messages":  len(result["queue"]),
                "rounds_elapsed":  result["current_round"],
            },
            "verified_agents": list(result['verified_agents']),
            "failed_decryptions": result['failed_decryptions'],
            "secret_messages": result['secret_messages'],
            "agent_ciphers": result['agent_ciphers'],
            "round_stats": result["round_stats"],
            "queue": [
                {k: v for k, v in item.items() if k != "id"}
                for item in result["queue"]
            ],
            "agent_contexts": {
                k: [msg.model_dump(include=['type', 'content', 'tool_calls', 'additional_kwargs']) for msg in v]
                for k, v in result['agent_contexts'].items()
            }
        }

        out_path = result['run_dir'] / file_name
    
        json_data = json.dumps(payload, indent=2, ensure_ascii=False)
        
        async with aiofiles.open(out_path, mode="w", encoding="utf-8") as f:
            await f.write(json_data)
            
        if self.verbose:
            print(f"Logs and results saved → {result['run_dir']}")


    async def log_summary(self, result: dict, topology: dict) -> None:
        await self.log('', result['run_dir'])
        await self.log("=" * 52, result['run_dir'])
        await self.log("EXPERIMENT RESULTS", result['run_dir'])
        await self.log("=" * 52, result['run_dir'])
        await self.log(f"Agents verified : {len(result['verified_agents'])}/{len(topology)}", result['run_dir'])
        await self.log(f"Total messages  : {len(result['queue'])}", result['run_dir'])
        await self.log(f"Rounds elapsed  : {result['current_round']}", result['run_dir'])
        await self.log('', result['run_dir'])
        await self.log(f"{'Round':<8} {'Msgs sent':>10} {'Active agents':>14} {'Verified':>10}", result['run_dir'])
        await self.log("-" * 46, result['run_dir'])
        for s in result["round_stats"]:
            await self.log(
                f"{s['round']:<8} {s['messages_sent']:>10}"
                f" {s['agents_active']:>14} {s['agents_verified']:>10}",
                result['run_dir']
            )


def create_run_dir(
    model_name: str,
    res_dir: str | Path,
    is_strict: bool,
    results_root: str | Path = "results",
) -> Path:
    sending_type = 'strict' if is_strict else 'free_text'
    run_dir = Path(results_root) / sending_type / res_dir / model_name
    run_dir.mkdir(parents=True, exist_ok=True)

    return run_dir
