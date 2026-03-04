"""
Executive Smary: Approximates Alternative Minimum Tax liability from preference items.
Inputs: regular_taxable_income (float), amt_preference_items (list), filing_status (str)
Outputs: amt_income (float), amt_exemption (float), tentative_minimum_tax (float), amt_liability (float), amt_crossover_income (float)
MCP Tool Name: amt_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

REGULAR_BRACKETS = {
    "single": [
        (0, 0.10),
        (11600, 0.12),
        (47150, 0.22),
        (100525, 0.24),
        (191950, 0.32),
        (243725, 0.35),
        (609350, 0.37),
    ],
    "mfj": [
        (0, 0.10),
        (23200, 0.12),
        (94300, 0.22),
        (201050, 0.24),
        (383900, 0.32),
        (487450, 0.35),
        (731200, 0.37),
    ],
}

AMT_EXEMPTIONS = {"single": 85700, "mfj": 133300}
AMT_PHASEOUT = {"single": 609350, "mfj": 1218700}


def _regular_tax(filing_status: str, taxable_income: float) -> float:
    brackets = REGULAR_BRACKETS[filing_status]
    tax = 0.0
    for idx, (threshold, rate) in enumerate(brackets):
        next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
        if taxable_income <= threshold:
            break
        upper = next_threshold if next_threshold is not None else taxable_income
        amount = min(taxable_income, upper) - threshold
        if amount <= 0:
            continue
        tax += amount * rate
    return tax


TOOL_META = {
    "name": "amt_calculator",
    "description": (
        "Calculates Alternative Minimum Tax income, exemption phase-out, tentative "
        "minimum tax, and resulting liability versus the regular tax system."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "regular_taxable_income": {
                "type": "number",
                "description": "Taxable income under regular rules.",
            },
            "amt_preference_items": {
                "type": "array",
                "description": "List of AMT add-backs (ISO spreads, state tax, etc.).",
                "items": {"type": "number"},
            },
            "filing_status": {
                "type": "string",
                "description": "single or mfj.",
            },
        },
        "required": ["regular_taxable_income", "amt_preference_items", "filing_status"],
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


def amt_calculator(**kwargs: Any) -> dict:
    """Estimate Alternative Minimum Tax liability based on preference items."""
    try:
        taxable_income = float(kwargs["regular_taxable_income"])
        preference_items = kwargs["amt_preference_items"]
        filing_status = str(kwargs["filing_status"]).strip().lower()

        if filing_status not in REGULAR_BRACKETS:
            raise ValueError("filing_status must be single or mfj")
        if not isinstance(preference_items, List):
            raise ValueError("amt_preference_items must be a list")

        add_backs = sum(float(item) for item in preference_items)
        amt_income = taxable_income + add_backs
        exemption = AMT_EXEMPTIONS[filing_status]
        phaseout_start = AMT_PHASEOUT[filing_status]
        if amt_income > phaseout_start:
            exemption = max(0.0, exemption - 0.25 * (amt_income - phaseout_start))
        taxable_amt = max(amt_income - exemption, 0.0)
        tentative_tax = (
            taxable_amt * 0.26 if taxable_amt <= 220700 else 220700 * 0.26 + (taxable_amt - 220700) * 0.28
        )
        regular_tax = _regular_tax(filing_status, taxable_income)
        amt_liability = max(tentative_tax - regular_tax, 0.0)
        amt_crossover = phaseout_start

        return {
            "status": "success",
            "data": {
                "amt_income": amt_income,
                "amt_exemption": exemption,
                "tentative_minimum_tax": tentative_tax,
                "amt_liability": amt_liability,
                "amt_crossover_income": amt_crossover,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"amt_calculator failed: {e}")
        _log_lesson(f"amt_calculator: {e}")
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
