"""Monitor basis between commodity spot and token prices.
Helps arbitrage desks understand tracking error."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "tokenized_commodity_basis_tracker",
    "description": "Compares token prices against spot commodity benchmarks adjusting for carry costs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "spot_price": {"type": "number", "description": "Benchmark spot price"},
            "token_price": {"type": "number", "description": "Market price of the commodity token"},
            "storage_cost_pct": {"type": "number", "description": "Annual storage/carry cost percent", "default": 0},
        },
        "required": ["spot_price", "token_price"],
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


def tokenized_commodity_basis_tracker(
    spot_price: float,
    token_price: float,
    storage_cost_pct: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Compute commodity basis vs token price.

    Args:
        spot_price: Reference commodity price.
        token_price: Price of tokenized exposure.
        storage_cost_pct: Annualized carry cost adjustment.

    Returns:
        Dict with basis levels and normalized spreads.
    """
    try:
        adjusted_spot = spot_price * (1 + storage_cost_pct / 100)
        basis = token_price - adjusted_spot
        basis_pct = basis / adjusted_spot * 100 if adjusted_spot else 0.0
        data = {
            "adjusted_spot": round(adjusted_spot, 4),
            "basis": round(basis, 4),
            "basis_pct": round(basis_pct, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("tokenized_commodity_basis_tracker failure: %s", exc)
        log_lesson(f"tokenized_commodity_basis_tracker: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
