"""Construct approval chains for Snowdrop actions."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "approval_chain_builder",
    "description": "Builds escalated approval chains based on action context and risk.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "action_type": {"type": "string"},
            "amount": {"type": "number"},
            "risk_level": {
                "type": "string",
                "enum": ["low", "medium", "high", "critical"],
                "default": "medium",
            },
        },
        "required": ["action_type"],
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


def approval_chain_builder(
    action_type: str,
    amount: float | None = None,
    risk_level: str = "medium",
    **_: Any,
) -> dict[str, Any]:
    """Return an ordered approver list with Thunder escalation rules."""
    try:
        risk_level = risk_level.lower()
        chain: list[dict[str, Any]]
        status: str

        if risk_level == "low":
            chain = [
                {
                    "role": "Automated policy",
                    "requirements": "Logging only",
                    "status": "auto",
                }
            ]
            status = "auto_approved"
        elif risk_level == "medium":
            chain = [
                {
                    "role": "Snowdrop CFO",
                    "requirements": "Ledger cross-check",
                    "status": "pending_thunder_approval",
                }
            ]
            status = "pending_cfo"
        elif risk_level == "high":
            chain = [
                {
                    "role": "Thunder",
                    "requirements": "2FA challenge",
                    "status": "pending_thunder_approval",
                }
            ]
            status = "pending_2fa"
        elif risk_level == "critical":
            chain = [
                {
                    "role": "Thunder",
                    "requirements": "2FA + ethics cool-down",
                    "status": "pending_thunder_approval",
                    "cool_down_minutes": 60,
                },
                {
                    "role": "Opus certifier",
                    "requirements": "Post-mortem certification",
                    "status": "pending",
                },
            ]
            status = "pending_multi_sig"
        else:
            raise ValueError("risk_level must be low, medium, high, or critical")

        extra_steps = _action_specific_steps(action_type, amount)
        chain.extend(extra_steps)

        data = {
            "action_type": action_type,
            "risk_level": risk_level,
            "amount": amount,
            "chain": chain,
            "status": status,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("approval_chain_builder", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _action_specific_steps(action_type: str, amount: float | None) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    normalized_amount = float(amount or 0.0)
    action_type = action_type.lower()

    if action_type in {"payment", "transfer"} and normalized_amount >= 10_000:
        steps.append(
            {
                "role": "Treasury",
                "requirements": "Payment packet validation",
                "status": "pending_thunder_approval",
            }
        )
    if action_type in {"trade", "deployment"} and normalized_amount >= 25_000:
        steps.append(
            {
                "role": "Ops multi-sig",
                "requirements": "3-of-5 approvers",
                "status": "pending_multi_sig",
            }
        )
    if action_type == "agent_onboarding":
        steps.append(
            {
                "role": "Compliance",
                "requirements": "KYC packet review",
                "status": "pending",
            }
        )
    return steps


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
