"""Estimate cross-chain bridge costs for a transfer.
Combines protocol base fees, percentage fees, and destination execution gas."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
import logging

from skills.utils import log_lesson

logger = logging.getLogger("snowdrop.skills")

TOOL_META: dict[str, Any] = {
    "name": "cross_chain_bridge_fee_estimator",
    "description": "Estimates total bridge fees including relayer markup and destination chain execution gas.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "transfer_amount": {"type": "number", "description": "Amount to transfer on source chain"},
            "base_fee": {"type": "number", "description": "Flat protocol fee"},
            "variable_fee_bps": {"type": "number", "description": "Basis point fee on transfer amount"},
            "relayer_markup_pct": {"type": "number", "description": "Relayer markup percent", "default": 0},
            "dst_gas_units": {"type": "number", "description": "Destination chain gas usage", "default": 0},
            "dst_gas_price_native": {"type": "number", "description": "Destination chain gas price in native token", "default": 0},
            "native_token_price_usd": {"type": "number", "description": "Destination native token USD price", "default": 0},
        },
        "required": ["transfer_amount", "base_fee", "variable_fee_bps"],
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


def cross_chain_bridge_fee_estimator(
    transfer_amount: float,
    base_fee: float,
    variable_fee_bps: float,
    relayer_markup_pct: float = 0.0,
    dst_gas_units: float = 0.0,
    dst_gas_price_native: float = 0.0,
    native_token_price_usd: float = 0.0,
    **_: Any,
) -> dict[str, Any]:
    """Sum bridge protocol fees and gas costs.

    Args:
        transfer_amount: Funds being bridged.
        base_fee: Flat fee denominated in transfer currency.
        variable_fee_bps: Basis point fee on transfer amount.
        relayer_markup_pct: Additional markup percent on total fees.
        dst_gas_units: Gas consumption on the destination chain.
        dst_gas_price_native: Gas price denominated in destination native token.
        native_token_price_usd: Fiat conversion for destination native token.

    Returns:
        Payload with fee stack and resulting take-rate.
    """
    try:
        percentage_fee = transfer_amount * variable_fee_bps / 10_000
        protocol_fee = base_fee + percentage_fee
        relayer_fee = protocol_fee * relayer_markup_pct / 100
        dst_gas_cost_native = dst_gas_units * dst_gas_price_native
        dst_gas_cost_usd = dst_gas_cost_native * native_token_price_usd
        total_fee = protocol_fee + relayer_fee + dst_gas_cost_usd
        data = {
            "protocol_fee": round(protocol_fee, 6),
            "relayer_fee": round(relayer_fee, 6),
            "dst_gas_cost_usd": round(dst_gas_cost_usd, 4),
            "total_fee": round(total_fee, 4),
            "take_rate_pct": round(total_fee / transfer_amount * 100 if transfer_amount else 0.0, 3),
        }
        return {"status": "success", "data": data, "timestamp": datetime.now(timezone.utc).isoformat()}
    except Exception as exc:  # noqa: BLE001
        logger.exception("cross_chain_bridge_fee_estimator failure: %s", exc)
        log_lesson(f"cross_chain_bridge_fee_estimator: {exc}")
        return {"status": "error", "error": str(exc), "timestamp": datetime.now(timezone.utc).isoformat()}
