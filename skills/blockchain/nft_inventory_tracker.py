"""Track Snowdrop's NFT holdings across TON and Solana."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "nft_inventory_tracker",
    "description": "Aggregates NFT holdings with valuation deltas and allocation mix.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "wallets": {
                "type": "array",
                "items": {"type": "object"},
            },
            "known_nfts": {
                "type": "array",
                "items": {"type": "object"},
            },
        },
        "required": ["wallets", "known_nfts"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "inventory": {"type": "array", "items": {"type": "object"}},
                    "total_estimated_value": {"type": "number"},
                },
            },
            "timestamp": {"type": "string"},
        },
    },
}


def nft_inventory_tracker(
    wallets: list[dict[str, Any]],
    known_nfts: list[dict[str, Any]],
    **_: Any,
) -> dict[str, Any]:
    """Return Snowdrop's NFT inventory annotated with gains/losses."""

    try:
        wallet_addresses = {wallet.get("address"): wallet.get("chain") for wallet in wallets}
        inventory: list[dict[str, Any]] = []
        total_value = 0.0
        for nft in known_nfts:
            wallet_address = nft.get("wallet_address")
            chain = wallet_addresses.get(wallet_address, nft.get("chain"))
            current_value = float(nft.get("current_value_estimate", 0))
            acquisition_cost = float(nft.get("acquisition_cost", 0))
            gain = current_value - acquisition_cost
            total_value += current_value
            inventory.append(
                {
                    "token_id": nft.get("token_id"),
                    "name": nft.get("name"),
                    "wallet_address": wallet_address,
                    "chain": chain,
                    "current_value": round(current_value, 2),
                    "acquisition_cost": round(acquisition_cost, 2),
                    "unrealized_gain_loss": round(gain, 2),
                }
            )

        total_value = round(total_value, 2)
        for entry in inventory:
            allocation = 0.0 if total_value == 0 else entry["current_value"] / total_value * 100
            entry["portfolio_allocation_pct"] = round(allocation, 3)

        data = {"inventory": inventory, "total_estimated_value": total_value}
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("nft_inventory_tracker", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
