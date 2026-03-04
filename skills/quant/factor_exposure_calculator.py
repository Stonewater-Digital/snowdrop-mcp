"""Estimate factor betas via single-factor regressions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "factor_exposure_calculator",
    "description": "Calculates factor betas and contribution to variance per factor.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_returns": {"type": "array", "items": {"type": "number"}},
            "factor_returns": {
                "type": "object",
                "additionalProperties": {
                    "type": "array",
                    "items": {"type": "number"},
                },
            },
        },
        "required": ["asset_returns", "factor_returns"],
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


def factor_exposure_calculator(asset_returns: list[float], factor_returns: dict[str, list[float]], **_: Any) -> dict[str, Any]:
    """Return betas and contributions per factor."""
    try:
        if not factor_returns:
            raise ValueError("factor_returns cannot be empty")
        target = [float(r) for r in asset_returns]
        length = len(target)
        if length < 2:
            raise ValueError("asset_returns must include at least two observations")
        exposures = []
        target_mean = sum(target) / length
        target_var = sum((r - target_mean) ** 2 for r in target)
        for factor, values in factor_returns.items():
            if len(values) != length:
                raise ValueError("factor series length mismatch")
            factor_series = [float(v) for v in values]
            factor_mean = sum(factor_series) / length
            var_factor = sum((v - factor_mean) ** 2 for v in factor_series)
            cov = sum((target[i] - target_mean) * (factor_series[i] - factor_mean) for i in range(length))
            beta = cov / var_factor if var_factor else 0.0
            contribution = beta**2 * var_factor / target_var if target_var else 0.0
            exposures.append(
                {
                    "factor": factor,
                    "beta": round(beta, 4),
                    "contribution_pct": round(contribution * 100, 2),
                }
            )
        data = {
            "exposures": exposures,
            "explained_variance_pct": round(sum(item["contribution_pct"] for item in exposures), 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        _log_lesson(f"factor_exposure_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
