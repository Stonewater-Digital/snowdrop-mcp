"""
Executive Summary: Validates construction loan draw requests by matching receipts to milestones and checking budget compliance.
Inputs: draw_request (dict: contractor, amount, milestone_id, receipts list), milestones (list of dicts: id, description, budget, completion_pct)
Outputs: dict with approved (bool), discrepancies (list), milestone_remaining_budget (float)
MCP Tool Name: construction_draw_validator
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "construction_draw_validator",
    "description": (
        "Validates a construction loan draw request by verifying that receipts "
        "sum to the requested amount, the milestone exists and has sufficient "
        "remaining budget, and completion percentage is consistent. "
        "Returns approval status, discrepancy list, and remaining milestone budget."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "draw_request": {
                "type": "object",
                "description": "Draw request submitted by the contractor.",
                "properties": {
                    "contractor":    {"type": "string"},
                    "amount":        {"type": "number"},
                    "milestone_id":  {"type": "string"},
                    "receipts": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "vendor": {"type": "string"},
                                "amount": {"type": "number"}
                            },
                            "required": ["vendor", "amount"]
                        }
                    }
                },
                "required": ["contractor", "amount", "milestone_id", "receipts"]
            },
            "milestones": {
                "type": "array",
                "description": "Master milestone schedule from the construction contract.",
                "items": {
                    "type": "object",
                    "properties": {
                        "id":              {"type": "string"},
                        "description":     {"type": "string"},
                        "budget":          {"type": "number"},
                        "completion_pct":  {"type": "number"}
                    },
                    "required": ["id", "description", "budget", "completion_pct"]
                }
            }
        },
        "required": ["draw_request", "milestones"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "approved":                   {"type": "boolean"},
                    "discrepancies":              {"type": "array"},
                    "milestone_remaining_budget":  {"type": "number"},
                    "receipts_total":             {"type": "number"}
                },
                "required": ["approved", "discrepancies", "milestone_remaining_budget"]
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "timestamp"]
    }
}

# Tolerance for floating point receipt/draw amount matching (dollars)
AMOUNT_TOLERANCE: float = 0.02

# Completion percentage that must be reached before a draw is approved (guard)
MIN_COMPLETION_PCT_FOR_DRAW: float = 0.0  # 0 = allow draws at any completion level


def construction_draw_validator(
    draw_request: dict,
    milestones: list[dict],
    **kwargs: Any
) -> dict:
    """Validate a construction loan draw request against milestone schedules.

    Checks performed:
    1. Milestone exists in the master schedule.
    2. Receipts are present and sum matches requested draw amount (within tolerance).
    3. Draw amount does not exceed remaining milestone budget.
    4. Milestone completion_pct >= MIN_COMPLETION_PCT_FOR_DRAW.
    5. Each receipt has a vendor name and positive amount.

    Args:
        draw_request: Dict with contractor (str), amount (float), milestone_id (str),
            receipts (list of dicts with vendor str and amount float).
        milestones: List of milestone dicts with id, description, budget,
            and completion_pct (0-100 scale).
        **kwargs: Ignored extra keyword arguments for MCP compatibility.

    Returns:
        dict with keys: status, data (approved, discrepancies, milestone_remaining_budget,
        receipts_total, milestone_budget, draw_amount, milestone_description), timestamp.

    Raises:
        ValueError: If draw_request or milestones are missing required fields.
    """
    try:
        # Validate draw_request fields
        for field in ("contractor", "amount", "milestone_id", "receipts"):
            if field not in draw_request:
                raise ValueError(f"draw_request missing required field '{field}'.")

        contractor: str = str(draw_request["contractor"])
        draw_amount: float = float(draw_request["amount"])
        milestone_id: str = str(draw_request["milestone_id"])
        receipts: list = draw_request["receipts"]

        if draw_amount <= 0:
            raise ValueError(f"draw_request.amount must be positive, got {draw_amount}")
        if not isinstance(receipts, list):
            raise ValueError("draw_request.receipts must be a list.")

        discrepancies: list[str] = []

        # --- Check 1: Milestone lookup ---
        milestone = None
        for m in milestones:
            if str(m.get("id", "")) == milestone_id:
                milestone = m
                break

        if milestone is None:
            discrepancies.append(
                f"Milestone ID '{milestone_id}' not found in master schedule. "
                f"Available IDs: {[str(m.get('id','')) for m in milestones]}."
            )
            return {
                "status": "success",
                "data": {
                    "approved": False,
                    "discrepancies": discrepancies,
                    "milestone_remaining_budget": 0.0,
                    "receipts_total": 0.0,
                    "draw_amount": draw_amount,
                    "contractor": contractor
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

        milestone_budget: float = float(milestone["budget"])
        milestone_desc: str = str(milestone.get("description", ""))
        completion_pct: float = float(milestone.get("completion_pct", 0))

        # --- Check 2: Receipts validation ---
        receipts_total: float = 0.0
        for i, receipt in enumerate(receipts):
            if not isinstance(receipt, dict):
                discrepancies.append(f"Receipt[{i}] is not a dict; skipped.")
                continue
            if "vendor" not in receipt or "amount" not in receipt:
                discrepancies.append(f"Receipt[{i}] missing 'vendor' or 'amount' field.")
                continue
            receipt_amt = float(receipt["amount"])
            if receipt_amt <= 0:
                discrepancies.append(
                    f"Receipt[{i}] from '{receipt.get('vendor','?')}' has non-positive amount {receipt_amt}."
                )
            receipts_total += receipt_amt

        if not receipts:
            discrepancies.append("No receipts provided. Draw requests must be backed by receipts.")

        # --- Check 3: Receipts total vs draw amount ---
        amount_diff = abs(receipts_total - draw_amount)
        if amount_diff > AMOUNT_TOLERANCE:
            discrepancies.append(
                f"Receipts total ${receipts_total:,.2f} does not match draw request "
                f"${draw_amount:,.2f} (diff=${amount_diff:,.2f}, tolerance=${AMOUNT_TOLERANCE})."
            )

        # --- Check 4: Budget sufficiency ---
        # Remaining budget = milestone_budget * (1 - completion_pct/100)
        # This simplifies to: a portion of the milestone budget not yet drawn
        # We treat milestone_budget as the TOTAL allocated and track against it directly
        milestone_remaining_budget: float = milestone_budget - draw_amount

        if draw_amount > milestone_budget:
            discrepancies.append(
                f"Draw amount ${draw_amount:,.2f} exceeds milestone budget "
                f"${milestone_budget:,.2f} by ${draw_amount - milestone_budget:,.2f}."
            )

        # --- Check 5: Completion percentage ---
        if completion_pct < MIN_COMPLETION_PCT_FOR_DRAW:
            discrepancies.append(
                f"Milestone completion is {completion_pct:.1f}%, below minimum "
                f"{MIN_COMPLETION_PCT_FOR_DRAW:.1f}% required for draw approval."
            )

        # --- Check 6: Completion-proportionality guard ---
        # Flag if draw exceeds the pro-rata earned amount
        if completion_pct > 0:
            earned_amount = milestone_budget * (completion_pct / 100.0)
            if draw_amount > earned_amount + AMOUNT_TOLERANCE:
                discrepancies.append(
                    f"Draw amount ${draw_amount:,.2f} exceeds earned amount "
                    f"${earned_amount:,.2f} based on {completion_pct:.1f}% completion "
                    f"of ${milestone_budget:,.2f} milestone budget."
                )

        approved: bool = len(discrepancies) == 0

        result: dict = {
            "approved": approved,
            "contractor": contractor,
            "milestone_id": milestone_id,
            "milestone_description": milestone_desc,
            "milestone_budget": round(milestone_budget, 2),
            "milestone_completion_pct": completion_pct,
            "draw_amount": round(draw_amount, 2),
            "receipts_total": round(receipts_total, 2),
            "receipt_count": len(receipts),
            "milestone_remaining_budget": round(milestone_remaining_budget, 2),
            "discrepancies": discrepancies,
            "discrepancy_count": len(discrepancies)
        }

        logger.info(
            "construction_draw_validator: milestone=%s, approved=%s, discrepancies=%d",
            milestone_id, approved, len(discrepancies)
        )

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

    except Exception as e:
        logger.error("construction_draw_validator failed: %s", e)
        _log_lesson(f"construction_draw_validator: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    """Append a lesson-learned entry to the shared lessons log.

    Args:
        message: Description of the error or lesson to record.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError as log_err:
        logger.warning("Could not write to lessons.md: %s", log_err)
