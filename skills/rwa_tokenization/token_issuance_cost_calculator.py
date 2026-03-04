"""Summarize costs incurred when issuing RWA tokens.
Supports budgeting numbers across legal, audit, and marketing components."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "token_issuance_cost_calculator",
    "description": "Aggregates issuance cost buckets and derives per-token cost of capital.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "legal_cost": {"type": "number", "description": "Legal and structuring fees"},
            "audit_cost": {"type": "number", "description": "Audit and attestation fees"},
            "marketing_cost": {"type": "number", "description": "Distribution and marketing spend"},
            "platform_fee": {"type": "number", "description": "Platform fee charged by issuance partner"},
            "tokens_issued": {"type": "number", "description": "Number of tokens minted"},
        },
        "required": ["legal_cost", "audit_cost", "marketing_cost", "platform_fee", "tokens_issued"],
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


def token_issuance_cost_calculator(
    legal_cost: float,
    audit_cost: float,
    marketing_cost: float,
    platform_fee: float,
    tokens_issued: float,
    **_: Any,
) -> dict[str, Any]:
    """Aggregate issuance costs.

    Args:
        legal_cost: Structuring legal spend.
        audit_cost: Assurance costs.
        marketing_cost: Investor marketing.
        platform_fee: Tokenization platform fee.
        tokens_issued: Tokens minted in the offering.

    Returns:
        Dict with total cost and per-token economics.
    """
    try:
        if tokens_issued <= 0:
            raise ValueError("tokens_issued must be positive")
        total_cost = legal_cost + audit_cost + marketing_cost + platform_fee
        cost_per_token = total_cost / tokens_issued
        data = {
            "total_cost": round(total_cost, 2),
            "cost_per_token": round(cost_per_token, 4),
            "cost_breakdown": {
                "legal": round(legal_cost, 2),
                "audit": round(audit_cost, 2),
                "marketing": round(marketing_cost, 2),
                "platform": round(platform_fee, 2),
            },
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("token_issuance_cost_calculator failure: %s", exc)
        log_lesson(f"token_issuance_cost_calculator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
