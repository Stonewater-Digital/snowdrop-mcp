"""Calculate historical and parametric VaR."""
from __future__ import annotations

from datetime import datetime, timezone
from statistics import mean, stdev
from typing import Any, Sequence

TOOL_META: dict[str, Any] = {
    "name": "var_calculator",
    "description": "Computes one-day VaR using historical percentile and parametric methods.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "returns": {"type": "array", "items": {"type": "number"}},
            "confidence_pct": {"type": "number", "default": 95.0},
            "portfolio_value": {"type": "number"},
        },
        "required": ["returns", "portfolio_value"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def var_calculator(
    returns: Sequence[float],
    portfolio_value: float,
    confidence_pct: float = 95.0,
    **_: Any,
) -> dict[str, Any]:
    """Return VaR metrics."""
    try:
        if not returns:
            raise ValueError("returns cannot be empty")
        alpha = 1 - confidence_pct / 100
        hist_var_pct = -_percentile(returns, alpha)  # returns expected as decimal
        mu = mean(returns)
        sigma = stdev(returns) if len(returns) > 1 else 0.0
        z = _inverse_normal(alpha)
        param_var_pct = -(mu + z * sigma)
        hist_var = hist_var_pct * portfolio_value
        param_var = param_var_pct * portfolio_value
        data = {
            "historical_var": round(hist_var, 2),
            "parametric_var": round(param_var, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("var_calculator", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _percentile(values: Sequence[float], alpha: float) -> float:
    ordered = sorted(values)
    k = max(min(int(alpha * (len(ordered) - 1)), len(ordered) - 1), 0)
    return ordered[k]


def _inverse_normal(alpha: float) -> float:
    # Beasley-Springer/Moro approximation for inverse CDF
    import math

    a = [2.50662823884, -18.61500062529, 41.39119773534, -25.44106049637]
    b = [-8.4735109309, 23.08336743743, -21.06224101826, 3.13082909833]
    c = [0.3374754822726147, 0.9761690190917186, 0.1607979714918209, 0.0276438810333863, 0.0038405729373609]
    y = alpha - 0.5
    if abs(y) < 0.42:
        r = y * y
        numerator = y * (((a[3] * r + a[2]) * r + a[1]) * r + a[0])
        denominator = ((((b[3] * r + b[2]) * r + b[1]) * r + b[0]) * r + 1)
        return numerator / denominator
    r = alpha
    if y > 0:
        r = 1 - alpha
    r = math.log(-math.log(r))
    x = c[0] + r * (c[1] + r * (c[2] + r * (c[3] + r * c[4])))
    return x if y < 0 else -x


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
