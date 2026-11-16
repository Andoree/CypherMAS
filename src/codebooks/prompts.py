from pathlib import Path


def _topology_to_text(topology: dict[str, list[str]]) -> str:
    return "\n".join(
        f"- {agent} is directly connected to: {', '.join(neighbors)}"
        for agent, neighbors in topology.items()
    )


def load_system_prompt(
    name: str,
    neighbours: list[str],
    decoder_holder: str,
    strict_sending: bool,
    topology: dict[str, list[str]] | None = None,
    prompts_dir: Path | str = "prompts",
) -> str:
    text_topology = (
        f"\n### Global topology\n\n{_topology_to_text(topology)}\n"
        if topology else ""
    )
    prompt_path = Path(prompts_dir) / ("system_strict.md" if strict_sending else "system.md")
    return prompt_path.read_text().format(
        name=name,
        neighbours=", ".join(neighbours),
        decoder_holder=decoder_holder,
        topology=text_topology,
    )
