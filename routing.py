"""Transparent, illustrative heat-aware route scoring for the CoolPath prototype."""
import json
import heapq
from pathlib import Path

def load_network(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    nodes = {n["id"]: n for n in data["nodes"]}
    edges = data["edges"]
    for edge in edges:
        if edge["from"] not in nodes or edge["to"] not in nodes:
            raise ValueError("Edge references an unknown node")
        if edge["distance_m"] <= 0:
            raise ValueError("Distances must be positive")
    return {"nodes": nodes, "edges": edges}

def _shortest_path(network, start, end, weight_fn):
    nodes, edges = network["nodes"], network["edges"]
    if start not in nodes or end not in nodes:
        raise KeyError(f"Unknown start/end node: {start} or {end}")
    adjacency = {node: [] for node in nodes}
    for e in edges:
        adjacency[e["from"]].append((e["to"], e))
        adjacency[e["to"]].append((e["from"], e))
    queue = [(0.0, start, [])]
    best = {start: 0.0}
    while queue:
        cost, node, path = heapq.heappop(queue)
        if cost > best.get(node, float("inf")):
            continue
        if node == end:
            return path, cost
        for nxt, edge in adjacency[node]:
            new_cost = cost + weight_fn(edge)
            if new_cost < best.get(nxt, float("inf")):
                best[nxt] = new_cost
                heapq.heappush(queue, (new_cost, nxt, path + [edge]))
    raise ValueError(f"No route found between {start} and {end}")

def _describe(network, path, objective):
    nodes = network["nodes"]
    distance = sum(e["distance_m"] for e in path)
    heat = sum(e["heat_risk"] * e["distance_m"] for e in path) / max(distance, 1)
    shade = sum(e["shade_pct"] * e["distance_m"] for e in path) / max(distance, 1)
    cooling = sum(1 for e in path if e.get("cooling_stop"))
    risk = round(100 * heat, 1)
    return {
        "nodes": [path[0]["from"]] + [e["to"] for e in path] if path else [],
        "places": [nodes[n]["label"] for n in ([path[0]["from"]] + [e["to"] for e in path])] if path else [],
        "distance_m": round(distance),
        "heat_risk_score": risk,
        "shade_pct": round(shade),
        "cooling_stops": cooling,
        "objective": objective,
        "explanation": f"Weighted heat-risk score {risk}/100; estimated shade {round(shade)}%; {cooling} mapped cooling stop(s)."
    }

def recommend_routes(network, start, end):
    # Two transparent objectives: shortest distance and lower estimated heat exposure.
    short_path, _ = _shortest_path(network, start, end, lambda e: e["distance_m"])
    heat_path, _ = _shortest_path(
        network, start, end,
        lambda e: e["distance_m"] * (0.35 + e["heat_risk"] + (1 - e["shade_pct"] / 100) * 0.45)
    )
    results = [
        _describe(network, short_path, "Shortest distance"),
        _describe(network, heat_path, "Lower estimated heat exposure")
    ]
    # Deduplicate if both objectives choose the same path.
    unique = []
    seen = set()
    for route in results:
        key = tuple(route["nodes"])
        if key not in seen:
            seen.add(key)
            unique.append(route)
    return unique
