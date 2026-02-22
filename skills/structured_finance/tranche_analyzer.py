"""Evaluate structured finance tranching and expected losses."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tranche_analyzer",
    "description": "Calculates tranche credit enhancement, expected loss, and implied ratings.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_pool": {"type": "number"},
            "expected_loss_pct": {"type": "number"},
            "loss_volatility": {"type": "number"},
            "tranches": {"type": "array", "items": {"type": "object"}},
        },
        "required": ["total_pool", "expected_loss_pct", "loss_volatility", "tranches"],
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


def tranche_analyzer(
    total_pool: float,
    expected_loss_pct: float,
    loss_volatility: float,
    tranches: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return tranche metrics including break-even loss rates."""
    try:
        losses = expected_loss_pct / 100 * total_pool
        tranches_sorted = sorted(tranches, key=lambda t: t.get("attachment_pct", 0))
        remaining_loss = losses
        tranche_results = []
        break_even = {}
        expected_loss_by_tranche = {}
        for tranche in tranches_sorted:
            attach = tranche.get("attachment_pct", 0) / 100 * total_pool
            detach = tranche.get("detachment_pct", 0) / 100 * total_pool
            thickness = detach - attach
            absorbed = max(min(remaining_loss - attach, thickness), 0)
            expected_loss_by_tranche[tranche.get("name") or "tranche"] = round(max(absorbed, 0), 2)
            break_even[tranche.get("name") or "tranche"] = tranche.get("detachment_pct", 0)
            enhancement = attach
            tranche_results.append(
                {
                    "name": tranche.get("name"),
                    "thickness": round(thickness, 2),
                    "expected_loss": round(max(absorbed, 0), 2),
                    "credit_enhancement": round(enhancement / total_pool * 100, 2),
                    "implied_rating": _rating_from_enhancement(enhancement / total_pool * 100),
                }
            )
        residual_equity_yield = max(total_pool - losses, 0) / total_pool * 100
        data = {
            "tranches": tranche_results,
            "total_credit_enhancement": {"pool": total_pool, "expected_loss": round(losses, 2)},
            "expected_loss_by_tranche": expected_loss_by_tranche,
            "break_even_loss_rate": break_even,
            "residual_equity_yield": round(residual_equity_yield, 2),
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("tranche_analyzer", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _rating_from_enhancement(enhancement_pct: float) -> str:
    if enhancement_pct > 35:
        return "AAA"
    if enhancement_pct > 25:
        return "AA"
    if enhancement_pct > 15:
        return "A"
    if enhancement_pct > 10:
        return "BBB"
    return "BB"


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
