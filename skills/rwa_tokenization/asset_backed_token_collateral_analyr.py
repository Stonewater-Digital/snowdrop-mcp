"""Check collateral sufficiency for asset-backed tokens.
Compares collateral value to token obligations under advance rates."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "asset_backed_token_collateral_analyr",
    "description": "Evaluates collateral value, advance rates, and haircuts for asset-backed token programs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "collateral_value": {"type": "number", "description": "Current collateral market value"},
            "token_outstanding": {"type": "number", "description": "Outstanding token liability"},
            "advance_rate_pct": {"type": "number", "description": "Max allowable advance rate"},
            "haircut_pct": {"type": "number", "description": "Risk haircut applied to collateral", "default": 0},
        },
        "required": ["collateral_value", "token_outstanding", "advance_rate_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
            "error": {"type": "string"},
        },
    },
}


def asset_backed_token_collateral_analyr(
    collateral_value: float,
    token_outstanding: float,
    advance_rate_pct: float,
    haircut_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Evaluate collateral coverage.

    Args:
        collateral_value: Market value of collateral backing tokens.
        token_outstanding: Liability represented by token holders.
        advance_rate_pct: Policy limit on leverage.
        haircut_pct: Additional risk haircut on collateral value.

    Returns:
        Dict summarizing borrowing base and deficit/surplus.
    """
    try:
        effective_collateral = collateral_value * (1 - haircut_pct / 100)
        borrowing_base = effective_collateral * advance_rate_pct / 100
        coverage_ratio = effective_collateral / token_outstanding if token_outstanding else float("inf")
        deficit = borrowing_base - token_outstanding
        data = {
            "effective_collateral": round(effective_collateral, 2),
            "borrowing_base": round(borrowing_base, 2),
            "coverage_ratio": round(coverage_ratio, 2) if coverage_ratio != float("inf") else float("inf"),
            "surplus_deficit": round(deficit, 2),
            "margin_call_flag": deficit < 0,
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("asset_backed_token_collateral_analyr failure: %s", exc)
        log_lesson(f"asset_backed_token_collateral_analyr: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
