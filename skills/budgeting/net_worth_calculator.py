"""Calculate personal net worth from assets and liabilities.

MCP Tool Name: net_worth_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "net_worth_calculator",
    "description": "Calculates net worth by subtracting total liabilities from total assets.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "assets": {
                "type": "array",
                "description": "List of assets with name and value.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "value": {"type": "number"},
                    },
                    "required": ["name", "value"],
                },
            },
            "liabilities": {
                "type": "array",
                "description": "List of liabilities with name and value.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "value": {"type": "number"},
                    },
                    "required": ["name", "value"],
                },
            },
        },
        "required": ["assets", "liabilities"],
    },
}


def net_worth_calculator(
    assets: list[dict[str, Any]], liabilities: list[dict[str, Any]]
) -> dict[str, Any]:
    """Calculates net worth from assets and liabilities."""
    try:
        total_assets = sum(a["value"] for a in assets)
        total_liabilities = sum(l["value"] for l in liabilities)
        net_worth = round(total_assets - total_liabilities, 2)

        asset_breakdown = sorted(
            [{"name": a["name"], "value": round(a["value"], 2)} for a in assets],
            key=lambda x: x["value"],
            reverse=True,
        )
        liability_breakdown = sorted(
            [{"name": l["name"], "value": round(l["value"], 2)} for l in liabilities],
            key=lambda x: x["value"],
            reverse=True,
        )

        debt_to_asset_ratio = round(total_liabilities / total_assets, 4) if total_assets > 0 else None

        return {
            "status": "ok",
            "data": {
                "net_worth": net_worth,
                "total_assets": round(total_assets, 2),
                "total_liabilities": round(total_liabilities, 2),
                "debt_to_asset_ratio": debt_to_asset_ratio,
                "asset_breakdown": asset_breakdown,
                "liability_breakdown": liability_breakdown,
                "assessment": "positive" if net_worth > 0 else "negative" if net_worth < 0 else "zero",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
