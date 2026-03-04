"""Project recurring royalty income for NFT collections.
Incorporates platform fees to estimate creator take rates."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "nft_royalty_cashflow_calculator",
    "description": "Calculates gross and net royalty cash flows using volume, pricing, and fee inputs.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "royalty_rate_pct": {"type": "number", "description": "Royalty percent applied on each sale"},
            "average_sale_price": {"type": "number", "description": "Average NFT sale price"},
            "monthly_sales": {"type": "number", "description": "Number of secondary sales per month"},
            "platform_fee_pct": {"type": "number", "description": "Marketplace fee percent", "default": 2.5},
        },
        "required": ["royalty_rate_pct", "average_sale_price", "monthly_sales"],
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


def nft_royalty_cashflow_calculator(
    royalty_rate_pct: float,
    average_sale_price: float,
    monthly_sales: float,
    platform_fee_pct: float = 2.5,
    **_: Any,
) -> dict[str, Any]:
    """Estimate monthly royalty inflows.

    Args:
        royalty_rate_pct: Royalty percentage per trade.
        average_sale_price: Typical sale price of the NFT collection.
        monthly_sales: Expected number of trades per month.
        platform_fee_pct: Marketplace rake percentage.

    Returns:
        Dict capturing gross royalties, net proceeds, and margin insights.
    """
    try:
        gross_volume = average_sale_price * monthly_sales
        gross_royalty = gross_volume * royalty_rate_pct / 100
        platform_fees = gross_volume * platform_fee_pct / 100
        net_royalty = gross_royalty - platform_fees
        data = {
            "gross_trading_volume": round(gross_volume, 2),
            "gross_royalty": round(gross_royalty, 2),
            "platform_fees": round(platform_fees, 2),
            "net_creator_cashflow": round(net_royalty, 2),
            "net_margin_pct": round((net_royalty / gross_volume * 100) if gross_volume else 0.0, 2),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("nft_royalty_cashflow_calculator failure: %s", exc)
        log_lesson(f"nft_royalty_cashflow_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
