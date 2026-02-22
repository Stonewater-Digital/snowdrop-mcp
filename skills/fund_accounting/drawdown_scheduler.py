"""
Executive Summary: Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline.

Inputs: total_commitment (float), called_to_date (float), upcoming_investments (list[dict]: name, amount, target_date)
Outputs: dict with next_call_amount (float), call_schedule (list), unfunded_commitment (float)
MCP Tool Name: drawdown_scheduler
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "drawdown_scheduler",
    "description": "Schedules capital call drawdowns based on unfunded commitment and upcoming investment pipeline.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "total_commitment": {
                "type": "number",
                "description": "Total LP capital commitment in dollars",
            },
            "called_to_date": {
                "type": "number",
                "description": "Capital already called/drawn in dollars",
            },
            "upcoming_investments": {
                "type": "array",
                "description": "Pipeline investments requiring capital calls",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Investment name"},
                        "amount": {"type": "number", "description": "Required capital in dollars"},
                        "target_date": {"type": "string", "description": "ISO date string (YYYY-MM-DD)"},
                    },
                    "required": ["name", "amount", "target_date"],
                },
            },
        },
        "required": ["total_commitment", "called_to_date", "upcoming_investments"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "next_call_amount": {"type": "number"},
            "call_schedule": {"type": "array"},
            "unfunded_commitment": {"type": "number"},
            "total_scheduled": {"type": "number"},
            "oversubscribed": {"type": "boolean"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "next_call_amount", "call_schedule", "unfunded_commitment",
            "total_scheduled", "oversubscribed", "status", "timestamp",
        ],
    },
}


def drawdown_scheduler(
    total_commitment: float,
    called_to_date: float,
    upcoming_investments: list[dict[str, Any]],
    **kwargs: Any,
) -> dict:
    """Schedules capital call drawdowns against unfunded LP commitment.

    Computes unfunded commitment (total_commitment - called_to_date), then
    iterates through upcoming investments sorted by target_date to build a
    call schedule. Calls are capped at the unfunded commitment. Flags if
    investments exceed available unfunded capital.

    Args:
        total_commitment: Total LP capital commitment in dollars.
        called_to_date: Capital already drawn in dollars.
        upcoming_investments: List of dicts with keys: name (str), amount (float),
            target_date (str, ISO date YYYY-MM-DD).
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains next_call_amount (float — the soonest scheduled call),
              call_schedule (list of call events), unfunded_commitment (float),
              total_scheduled (float), oversubscribed (bool), status, timestamp.
    """
    try:
        if total_commitment <= 0:
            raise ValueError("total_commitment must be positive")
        if called_to_date < 0:
            raise ValueError("called_to_date cannot be negative")
        if called_to_date > total_commitment:
            raise ValueError("called_to_date cannot exceed total_commitment")

        unfunded_commitment = total_commitment - called_to_date
        pct_called = called_to_date / total_commitment

        # Sort investments by target date ascending
        sorted_investments = sorted(
            upcoming_investments,
            key=lambda x: x.get("target_date", "9999-12-31"),
        )

        call_schedule: list[dict] = []
        cumulative_called = 0.0
        total_needed = sum(float(inv["amount"]) for inv in sorted_investments)
        oversubscribed = total_needed > unfunded_commitment

        for inv in sorted_investments:
            name = inv["name"]
            amount = float(inv["amount"])
            target_date = inv.get("target_date", "")

            if amount <= 0:
                raise ValueError(f"Investment '{name}' amount must be positive")

            remaining_unfunded = unfunded_commitment - cumulative_called
            callable_amount = min(amount, remaining_unfunded)
            shortfall = max(0.0, amount - callable_amount)
            cumulative_called += callable_amount

            call_schedule.append({
                "investment": name,
                "required_amount": round(amount, 2),
                "callable_amount": round(callable_amount, 2),
                "shortfall": round(shortfall, 2),
                "target_date": target_date,
                "cumulative_called_post": round(called_to_date + cumulative_called, 2),
                "pct_of_commitment": round((called_to_date + cumulative_called) / total_commitment, 6),
            })

        next_call_amount = call_schedule[0]["callable_amount"] if call_schedule else 0.0
        total_scheduled = round(sum(c["callable_amount"] for c in call_schedule), 2)

        result = {
            "unfunded_commitment": round(unfunded_commitment, 2),
            "called_to_date": round(called_to_date, 2),
            "total_commitment": round(total_commitment, 2),
            "pct_called_to_date": round(pct_called, 6),
            "next_call_amount": round(next_call_amount, 2),
            "total_scheduled": total_scheduled,
            "total_needed_for_pipeline": round(total_needed, 2),
            "oversubscribed": oversubscribed,
            "call_schedule": call_schedule,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"drawdown_scheduler failed: {e}")
        _log_lesson(f"drawdown_scheduler: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
