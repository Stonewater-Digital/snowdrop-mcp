"""
Executive Smary: Identifies current federal tax bracket and headroom to the next tier.
Inputs: taxable_income (float), filing_status (str)
Outputs: current_bracket (str), marginal_rate (float), headroom_to_next_bracket (float), effective_rate (float), bracket_visualization (list)
MCP Tool Name: tax_bracket_marginal_analyzer
"""
import logging
from datetime import datetime, timezone
from typing import Any, List, Tuple

logger = logging.getLogger("snowdrop.skills")

BRACKETS = {
    "single": [
        (0, 0.10, "10%"),
        (11600, 0.12, "12%"),
        (47150, 0.22, "22%"),
        (100525, 0.24, "24%"),
        (191950, 0.32, "32%"),
        (243725, 0.35, "35%"),
        (609350, 0.37, "37%"),
    ],
    "mfj": [
        (0, 0.10, "10%"),
        (23200, 0.12, "12%"),
        (94300, 0.22, "22%"),
        (201050, 0.24, "24%"),
        (383900, 0.32, "32%"),
        (487450, 0.35, "35%"),
        (731200, 0.37, "37%"),
    ],
}


def _effective_rate(brackets: List[Tuple[float, float, str]], income: float) -> float:
    tax = 0.0
    for idx, (threshold, rate, _) in enumerate(brackets):
        next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
        if income <= threshold:
            break
        upper = next_threshold if next_threshold is not None else income
        amount = min(income, upper) - threshold
        if amount <= 0:
            continue
        tax += amount * rate
    return tax / income if income > 0 else 0.0


TOOL_META = {
    "name": "tax_bracket_marginal_analyzer",
    "description": (
        "Reports the taxpayer's current federal bracket, marginal rate, remaining income "
        "headroom before the next bracket, and a visualization of all bracket tiers."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "taxable_income": {
                "type": "number",
                "description": "Income after deductions subject to federal tax.",
            },
            "filing_status": {
                "type": "string",
                "description": "single or mfj.",
            },
        },
        "required": ["taxable_income", "filing_status"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
            "data": {"type": "object"},
        },
        "required": ["status", "timestamp"],
    },
}


def tax_bracket_marginal_analyzer(**kwargs: Any) -> dict:
    """Identify marginal tax rate and next bracket headroom."""
    try:
        taxable_income = float(kwargs["taxable_income"])
        filing_status = str(kwargs["filing_status"]).strip().lower()

        if filing_status not in BRACKETS:
            raise ValueError("filing_status must be single or mfj")
        if taxable_income < 0:
            raise ValueError("taxable_income must be non-negative")

        brackets = BRACKETS[filing_status]
        current_bracket = brackets[0]
        headroom = float("inf")
        for idx, (threshold, rate, label) in enumerate(brackets):
            next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
            if taxable_income >= threshold:
                current_bracket = (threshold, rate, label)
                if next_threshold:
                    headroom = max(next_threshold - taxable_income, 0.0)
                else:
                    headroom = float("inf")
        marginal_rate = current_bracket[1]
        current_bracket_label = current_bracket[2]
        visualization = []
        for idx, (threshold, rate, label) in enumerate(brackets):
            next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
            visualization.append(
                {
                    "label": label,
                    "rate": rate,
                    "lower_bound": threshold,
                    "upper_bound": next_threshold if next_threshold is not None else None,
                }
            )

        return {
            "status": "success",
            "data": {
                "current_bracket": current_bracket_label,
                "marginal_rate": marginal_rate,
                "headroom_to_next_bracket": headroom,
                "effective_rate": _effective_rate(brackets, taxable_income),
                "bracket_visualization": visualization,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"tax_bracket_marginal_analyzer failed: {e}")
        _log_lesson(f"tax_bracket_marginal_analyzer: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
