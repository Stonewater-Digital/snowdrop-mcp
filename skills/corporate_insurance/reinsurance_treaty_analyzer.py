"""Corporate reinsurance treaty analyzer.
Evaluates quota share vs excess structures for enterprise programs.
"""
from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "reinsurance_treaty_analyzer",
    "description": "Compares QS and XL treaties for cost, protection, and leverage impacts.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "treaty_type": {"type": "string", "enum": ["quota_share", "excess_of_loss"]},
            "gross_losses": {"type": "number"},
            "gross_premium": {"type": "number"},
            "cession_pct": {"type": "number", "default": 0.0},
            "retention": {"type": "number", "default": 0.0},
            "limit": {"type": "number", "default": 0.0},
        },
        "required": ["treaty_type", "gross_losses", "gross_premium"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {"status": {"type": "string"}, "data": {"type": "object"}, "timestamp": {"type": "string"}},
    },
}


def reinsurance_treaty_analyzer(
    treaty_type: str,
    gross_losses: float,
    gross_premium: float,
    cession_pct: float = 0.0,
    retention: float = 0.0,
    limit: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Return ceded/retained metrics based on treaty selection."""
    try:
        treaty_type = treaty_type.lower()
        if treaty_type == "quota_share":
            ceded_premium = gross_premium * cession_pct / 100
            ceded_loss = gross_losses * cession_pct / 100
            net_premium = gross_premium - ceded_premium
            net_loss = gross_losses - ceded_loss
        else:
            retention_limit = retention
            layer_limit = limit
            ceded_loss = min(max(gross_losses - retention_limit, 0.0), layer_limit)
            net_loss = gross_losses - ceded_loss
            ceded_premium = ceded_loss * 0.3
            net_premium = gross_premium - ceded_premium
        net_combined_ratio = net_loss / net_premium if net_premium else 0.0
        protection_ratio = ceded_loss / gross_losses if gross_losses else 0.0
        data = {
            "ceded_premium": round(ceded_premium, 2),
            "ceded_loss": round(ceded_loss, 2),
            "net_premium": round(net_premium, 2),
            "net_loss": round(net_loss, 2),
            "protection_ratio_pct": round(protection_ratio * 100, 2),
            "net_combined_ratio": round(net_combined_ratio, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("reinsurance_treaty_analyzer failed")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
