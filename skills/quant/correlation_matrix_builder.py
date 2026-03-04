"""Build correlation matrix from asset return series."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "correlation_matrix_builder",
    "description": "Generates pairwise correlation matrix and summary statistics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns_by_asset": {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            }
        },
        "required": ["returns_by_asset"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def correlation_matrix_builder(returns_by_asset: dict[str, list[float]], **_: Any) -> dict[str, Any]:
    """Return correlation matrix and diagnostics."""
    try:
        assets = list(returns_by_asset)
        if len(assets) < 2:
            raise ValueError("Need at least two assets to compute correlation")
        lengths = {len([float(x) for x in returns_by_asset[a]]) for a in assets}
        if len(lengths) != 1:
            raise ValueError("All series must be the same length")
        length = lengths.pop()
        if length < 2:
            raise ValueError("Need at least two observations per series")
        normalized = {asset: [float(x) for x in returns_by_asset[asset]] for asset in assets}
        means = {asset: sum(series) / length for asset, series in normalized.items()}
        corr_matrix: list[list[float]] = []
        summary_pairs: list[tuple[str, str, float]] = []
        for asset_i in assets:
            row = []
            for asset_j in assets:
                if asset_i == asset_j:
                    row.append(1.0)
                    continue
                cov = sum((normalized[asset_i][k] - means[asset_i]) * (normalized[asset_j][k] - means[asset_j]) for k in range(length))
                var_i = sum((normalized[asset_i][k] - means[asset_i]) ** 2 for k in range(length))
                var_j = sum((normalized[asset_j][k] - means[asset_j]) ** 2 for k in range(length))
                corr = cov / (var_i ** 0.5 * var_j ** 0.5) if var_i and var_j else 0.0
                row.append(round(corr, 4))
                summary_pairs.append((asset_i, asset_j, corr))
            corr_matrix.append(row)
        abs_pairs = [(a, b, abs(v)) for a, b, v in summary_pairs if a < b]
        hottest = max(abs_pairs, key=lambda item: item[2], default=("", "", 0.0))
        avg_abs = sum(pair[2] for pair in abs_pairs) / len(abs_pairs) if abs_pairs else 0.0
        data = {
            "assets": assets,
            "correlation_matrix": corr_matrix,
            "average_absolute_correlation": round(avg_abs, 3),
            "highest_correlation_pair": {"pair": [hottest[0], hottest[1]], "abs_value": round(hottest[2], 3)},
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"correlation_matrix_builder: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
