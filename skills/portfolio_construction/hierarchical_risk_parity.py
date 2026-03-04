"""
Executive Summary: Hierarchical Risk Parity allocator using Lopez de Prado's tree clustering to equalize risk across clusters.
Inputs: asset_returns (dict[str, list[float]]), min_periods (int), linkage (str)
Outputs: hrp_weights (list[dict]), covariance_matrix (list[list[float]]), dendrogram (list[dict]), cluster_risk (list[dict])
MCP Tool Name: hierarchical_risk_parity
"""
import logging
from datetime import datetime, timezone
from math import sqrt
from typing import Any, Dict, List

import numpy as np

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "hierarchical_risk_parity",
    "description": (
        "Constructs Lopez de Prado's Hierarchical Risk Parity (HRP) allocation with "
        "single-linkage clustering and recursive bisection risk budgeting."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_returns": {
                "type": "object",
                "description": "Dictionary of asset identifiers to historical return series (decimal).",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number", "description": "Return observation"},
                },
            },
            "min_periods": {
                "type": "integer",
                "description": "Minimum observations required per asset (default 60).",
            },
            "linkage": {
                "type": "string",
                "description": "Linkage criterion: single or average (default single).",
            },
        },
        "required": ["asset_returns"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "Execution status"},
            "data": {"type": "object", "description": "Allocations and diagnostics"},
            "timestamp": {"type": "string", "description": "UTC timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def _validate_series(asset_returns: Dict[str, List[float]], min_periods: int) -> List[str]:
    labels = []
    lengths = set()
    for label, series in asset_returns.items():
        arr = list(series)
        if len(arr) < max(2, min_periods):
            raise ValueError(f"Asset {label} has insufficient history")
        labels.append(label)
        lengths.add(len(arr))
    if len(lengths) != 1:
        raise ValueError("All assets must share the same observation count")
    return labels


def _distance(corr: np.ndarray) -> np.ndarray:
    dist = np.sqrt(np.maximum(0.0, 0.5 * (1 - corr)))
    np.fill_diagonal(dist, 0.0)
    return dist


def _cluster_distance(a: List[int], b: List[int], dist: np.ndarray, method: str) -> float:
    pairs = [dist[i, j] for i in a for j in b]
    if method == "average":
        return float(sum(pairs) / len(pairs))
    return float(min(pairs))


def _hierarchical_linkage(
    dist: np.ndarray, linkage: str
) -> tuple[List[Dict[str, Any]], Dict[int, List[int]]]:
    n = dist.shape[0]
    clusters = {i: [i] for i in range(n)}
    active = list(range(n))
    next_id = n
    tree: List[Dict[str, Any]] = []
    while len(active) > 1:
        best_pair = None
        best_distance = float("inf")
        for idx, left in enumerate(active[:-1]):
            for right in active[idx + 1 :]:
                d = _cluster_distance(clusters[left], clusters[right], dist, linkage)
                if d < best_distance:
                    best_distance = d
                    best_pair = (left, right)
        left, right = best_pair  # type: ignore
        tree.append({"parent": next_id, "left": left, "right": right, "distance": best_distance})
        clusters[next_id] = clusters[left] + clusters[right]
        active = [c for c in active if c not in (left, right)]
        active.append(next_id)
        next_id += 1
    return tree, clusters


def _extract_order(tree: List[Dict[str, Any]], n_assets: int) -> List[int]:
    if n_assets == 1:
        return [0]
    children = {node["parent"]: (node["left"], node["right"]) for node in tree}
    root = tree[-1]["parent"] if tree else 0

    def _recurse(node: int) -> List[int]:
        if node < n_assets:
            return [node]
        left, right = children[node]
        return _recurse(left) + _recurse(right)

    return _recurse(root)


def _cluster_variance(cov: np.ndarray, indices: List[int]) -> float:
    sub = cov[np.ix_(indices, indices)]
    inv_diag = 1 / np.diag(sub)
    weights = inv_diag / inv_diag.sum()
    return float(weights.T @ sub @ weights)


def _hrp_allocation(cov: np.ndarray, order: List[int]) -> np.ndarray:
    w = np.ones(len(order))
    clusters = [order]
    while clusters:
        cluster = clusters.pop(0)
        if len(cluster) == 1:
            continue
        split = len(cluster) // 2
        left = cluster[:split]
        right = cluster[split:]
        var_left = _cluster_variance(cov, left)
        var_right = _cluster_variance(cov, right)
        total = var_left + var_right
        if total <= 0:
            alpha = 0.5
        else:
            alpha = 1 - var_left / total
        for idx in left:
            w[order.index(idx)] *= alpha
        for idx in right:
            w[order.index(idx)] *= 1 - alpha
        clusters.append(left)
        clusters.append(right)
    full_weights = np.zeros(len(order))
    for idx, asset_index in enumerate(order):
        full_weights[asset_index] = w[idx]
    full_weights = full_weights / full_weights.sum()
    return full_weights


def hierarchical_risk_parity(
    asset_returns: Dict[str, List[float]],
    min_periods: int = 60,
    linkage: str = "single",
    **_: Any,
) -> dict[str, Any]:
    try:
        if linkage not in {"single", "average"}:
            raise ValueError("linkage must be 'single' or 'average'")
        labels = _validate_series(asset_returns, min_periods)
        matrix = np.array([asset_returns[label] for label in labels], dtype=float)
        cov = np.cov(matrix)
        corr = np.corrcoef(matrix)
        dist = _distance(corr)
        tree, cluster_map = _hierarchical_linkage(dist, linkage)
        order = _extract_order(tree, len(labels))
        weights = _hrp_allocation(cov, order)
        cluster_risk = []
        for node in tree:
            members = cluster_map.get(node["parent"], [])
            if members:
                var = _cluster_variance(cov, members)
                cluster_risk.append({"cluster": [labels[i] for i in members], "variance": round(var, 8)})

        data = {
            "hrp_weights": [{"asset": labels[idx], "weight": round(weight, 6)} for idx, weight in enumerate(weights)],
            "covariance_matrix": cov.round(8).tolist(),
            "correlation_matrix": corr.round(8).tolist(),
            "dendrogram": tree,
            "cluster_risk": cluster_risk,
            "ordering": [labels[i] for i in order],
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"hierarchical_risk_parity failed: {e}")
        _log_lesson(f"hierarchical_risk_parity: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
