import random
from collections import deque
from typing import Literal

import numpy as np
from scipy.optimize import linear_sum_assignment


default_names = [
    "Alice", "Bob", "Carol", "Eve", "Mallory", "Trent",
    "Charlie", "Dave", "Oscar", "Trudy", "Peggy", "Victor",
    "Frank", "Grace", "Heidi", "Ivan", "Judy", "Mike", 
    "Olivia", "Rupert", "Sybil", "Walter", "Wendy", "Arthur", "Zoe"
]

TopologyType = Literal["chain", "ring", "fc", "bipartite", "star", "tree"]


def make_topology(num_agents: int, topology_type: TopologyType) -> dict[str, list[str]]:
    if num_agents > len(default_names):
        names = [f'agent_{i}' for i in range(num_agents)]
    else:
        names = default_names[:num_agents]

    if topology_type == 'chain':
        topology = {}
        for i, name in enumerate(names):
            neighbors = []
            if i > 0:
                neighbors.append(names[i - 1])
            if i < num_agents - 1:
                neighbors.append(names[i + 1])
            topology[name] = neighbors
    elif topology_type == 'ring':
        topology = {
            name: [names[(i-1) % num_agents], names[(i+1) % num_agents]]
            for i, name in enumerate(names)
        }
    elif topology_type == 'fc':
        topology = {name: [o for o in names if o != name] for name in names}
    elif topology_type == 'star':
        hub, leaves = names[0], names[1:]
        topology = {hub: list(leaves), **{leaf: [hub] for leaf in leaves}}
    elif topology_type == 'bipartite':
        mid = num_agents // 2
        left, right = names[:mid], names[mid:]
        topology = {**{n: list(right) for n in left}, **{n: list(left) for n in right}}
    elif topology_type == 'tree':
        topology = {}
        for i, name in enumerate(names):
            neighbors = []
            if i > 0:
                neighbors.append(names[(i - 1) // 2])
            left = 2 * i + 1
            if left < num_agents:
                neighbors.append(names[left])
            right = 2 * i + 2
            if right < num_agents:
                neighbors.append(names[right])
            topology[name] = neighbors
    else:
        raise ValueError(f"Unknown topology type: {topology_type}")

    return topology


def _all_pairs_shortest_paths(graph: dict[str, list[str]]) -> dict[str, dict[str, int]]:
    distances = {}
    for start in graph:
        dist = {start: 0}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        distances[start] = dist
    return distances


def assign_decoders(
    graph: dict[str, list[str]],
    mode: Literal["max", "min", "random"] = "max",
    seed: int = 42,
) -> dict[str, str]:
    """Return {agent: decoder_holder} — who holds the decoder for each agent."""
    nodes = list(graph)
    n = len(nodes)
    if n < 2:
        raise ValueError("Needs at least 2 agents")

    if mode == "random":
        rng = random.Random(seed)
        while True:
            perm = nodes[:]
            rng.shuffle(perm)
            if all(a != b for a, b in zip(nodes, perm)):
                return dict(zip(nodes, perm))

    distances = _all_pairs_shortest_paths(graph)
    cost = np.zeros((n, n))
    for i, src in enumerate(nodes):
        for j, dst in enumerate(nodes):
            if src == dst:
                cost[i, j] = 1e9
                continue
            dist = distances[src][dst]
            cost[i, j] = -dist if mode == "max" else dist

    rows, cols = linear_sum_assignment(cost)
    return {nodes[i]: nodes[j] for i, j in zip(rows, cols)}


def visualize_topology(
    topology: dict[str, list[str]],
    decoder_holders: dict[str, str] | None = None,
    figsize: tuple[int, int] = (10, 8),
) -> None:
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.Graph()
    for node, neighbors in topology.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=figsize)
    nx.draw_networkx_nodes(G, pos, node_size=3500)
    nx.draw_networkx_edges(G, pos, width=2)

    if decoder_holders:
        stored_decoders = {holder: owner for owner, holder in decoder_holders.items()}
        labels = {
            node: f"{node}\nholds: {stored_decoders.get(node, '-')}"
            for node in G.nodes
        }
        DG = nx.DiGraph()
        for owner, holder in decoder_holders.items():
            DG.add_edge(owner, holder)
        nx.draw_networkx_edges(
            DG, pos,
            edge_color="red", style="dashed", width=1,
            arrows=True, arrowstyle="-|>", arrowsize=30,
            connectionstyle="arc3,rad=0.25",
            min_source_margin=20, min_target_margin=20,
        )
    else:
        labels = {node: node for node in G.nodes}

    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)
    plt.title("Topology and Decoder Placement")
    plt.axis("off")
    plt.tight_layout()
    plt.show()
