"""
Executive Summary: CCP default fund sizing satisfying cover-2 requirement (largest two members under stress).
Inputs: clearing_members (list[dict]), margin_held (float)
Outputs: default_fund_size (float), member_contributions (list[dict]), cover_two_shortfall (float)
MCP Tool Name: default_fund_sizing
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "default_fund_sizing",
    "description": "Computes cover-2 requirement using member stress losses net of margin and allocates contributions.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "clearing_members": {
                "type": "array",
                "description": "Members with stress loss estimates and current margin.",
                "items": {
                    "type": "object",
                    "properties": {
                        "member": {"type": "string", "description": "Member identifier"},
                        "stress_loss": {"type": "number", "description": "Loss under cover scenario"},
                        "initial_margin": {"type": "number", "description": "Margin posted by member"},
                        "guaranty_fund_contribution": {"type": "number", "description": "Existing contribution"},
                    },
                    "required": ["member", "stress_loss", "initial_margin"],
                },
            },
            "margin_held": {
                "type": "number",
                "description": "Aggregate initial margin held by CCP.",
            },
        },
        "required": ["clearing_members", "margin_held"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Default fund metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def default_fund_sizing(
    clearing_members: List[dict[str, Any]],
    margin_held: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not clearing_members:
            raise ValueError("clearing_members required")
        net_losses = [max(member["stress_loss"] - member["initial_margin"], 0.0) for member in clearing_members]
        cover_two = sum(sorted(net_losses, reverse=True)[:2])
        shortfall = max(cover_two - margin_held, 0.0)
        total_contribution = sum(member.get("guaranty_fund_contribution", 0.0) for member in clearing_members)
        contributions = []
        stress_total = sum(m["stress_loss"] for m in clearing_members)
        if shortfall > 0:
            for member in clearing_members:
                weight = member.get("stress_loss", 0.0) / stress_total if stress_total else 0.0
                contribution = shortfall * weight
                contributions.append(
                    {
                        "member": member["member"],
                        "additional_contribution": round(contribution, 2),
                        "net_stress_loss": round(max(member["stress_loss"] - member["initial_margin"], 0.0), 2),
                    }
                )
        data = {
            "cover_two_requirement": round(cover_two, 2),
            "margin_held": round(margin_held, 2),
            "default_fund_size": round(max(shortfall, total_contribution), 2),
            "cover_two_shortfall": round(shortfall, 2),
            "member_contributions": contributions,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"default_fund_sizing failed: {e}")
        _log_lesson(f"default_fund_sizing: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
