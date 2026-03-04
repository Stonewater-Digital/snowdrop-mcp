"""Price CDS spreads and implied default probabilities."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_default_swap_pricer",
    "description": "Converts CDS spreads into implied default probabilities and expected losses.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "cds_spread_bps": {"type": "integer"},
            "recovery_rate": {"type": "number", "default": 0.4},
            "notional": {"type": "number"},
            "maturity_years": {"type": "integer"},
            "payment_frequency": {"type": "string", "enum": ["quarterly"], "default": "quarterly"},
        },
        "required": ["cds_spread_bps", "recovery_rate", "notional", "maturity_years"],
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}}},
}


def credit_default_swap_pricer(
    cds_spread_bps: int,
    notional: float,
    maturity_years: int,
    recovery_rate: float = 0.4,
    **_: Any,
) -> dict[str, Any]:
    """Return CDS default probability and premium stats."""
    try:
        spread = cds_spread_bps / 10000
        annual_pd = spread / max(1 - recovery_rate, 0.01)
        cumulative_pd = 1 - (1 - annual_pd) ** maturity_years
        annual_premium = notional * spread
        expected_loss = notional * cumulative_pd * (1 - recovery_rate)
        quality = "IG" if spread < 0.015 else "HY"
        data = {
            "annual_default_prob": round(annual_pd, 4),
            "cumulative_default_prob": round(cumulative_pd, 4),
            "annual_premium": round(annual_premium, 2),
            "expected_loss": round(expected_loss, 2),
            "credit_quality_implied": quality,
            "sd_per_expected_loss": round(spread / max(expected_loss / notional, 0.0001), 2),
            "basis_analysis": None,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:
        _log_lesson("credit_default_swap_pricer", str(exc))
        return {"status": "error", "data": {"error": str(exc)}, "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
