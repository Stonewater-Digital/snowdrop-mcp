"""
Executive Smary: Estimates US federal income tax liability using 2024 brackets.
Inputs: filing_status (str), gross_income (float), above_line_deductions (float), itemized_deductions (float|None)
Outputs: agi (float), taxable_income (float), tax_liability (float), effective_rate (float), marginal_rate (float), bracket_breakdown (list), standard_vs_itemized (dict)
MCP Tool Name: federal_income_tax_estimator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

logger = logging.getLogger("snowdrop.skills")

STANDARD_DEDUCTION = {
    "single": 14600,
    "mfj": 29200,
    "mfs": 14600,
    "hoh": 21900,
}

BRACKETS: Dict[str, List[Tuple[float, float]]] = {
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
    "mfs": [
        (0, 0.10),
        (11600, 0.12),
        (47150, 0.22),
        (100525, 0.24),
        (191950, 0.32),
        (243725, 0.35),
        (365600, 0.37),
    ],
    "hoh": [
        (0, 0.10),
        (16550, 0.12),
        (63100, 0.22),
        (100500, 0.24),
        (191950, 0.32),
        (243700, 0.35),
        (609350, 0.37),
    ],
}


def _compute_tax(brackets: List[Tuple[float, float]], taxable: float) -> tuple[float, float, List[dict]]:
    tax = 0.0
    breakdown = []
    marginal_rate = 0.0
    remaining = taxable
    for idx, (threshold, rate) in enumerate(brackets):
        next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
        if taxable <= threshold:
            break
        upper_bound = next_threshold if next_threshold is not None else taxable
        amount = min(taxable, upper_bound) - threshold
        if amount <= 0:
            continue
        tax_piece = amount * rate
        tax += tax_piece
        marginal_rate = rate
        breakdown.append({"rate": rate, "amount_taxed": amount, "tax": tax_piece})
        remaining -= amount
        if remaining <= 0 or next_threshold is None:
            break
    return tax, marginal_rate, breakdown


TOOL_META = {
    "name": "federal_income_tax_estimator",
    "description": (
        "Applies 2024 U.S. federal tax brackets to compute AGI, taxable income, tax "
        "liability, marginal rate, and bracket-level breakdown."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "filing_status": {
                "type": "string",
                "description": "single, mfj, mfs, or hoh.",
            },
            "gross_income": {
                "type": "number",
                "description": "Total income prior to adjustments.",
            },
            "above_line_deductions": {
                "type": "number",
                "description": "Adjustments to income (401k, HSA, etc.).",
            },
            "itemized_deductions": {
                "type": "number",
                "description": "Optional itemized deductions; if omitted, standard is used.",
            },
        },
        "required": ["filing_status", "gross_income", "above_line_deductions"],
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


def federal_income_tax_estimator(**kwargs: Any) -> dict:
    """Estimate 2024 federal tax for major filing statuses."""
    try:
        filing_status = str(kwargs["filing_status"]).strip().lower()
        gross_income = float(kwargs["gross_income"])
        above_line = float(kwargs["above_line_deductions"])
        itemized = kwargs.get("itemized_deductions")
        itemized_amount = float(itemized) if itemized is not None else None

        if filing_status not in BRACKETS:
            raise ValueError("Unsupported filing_status")
        if gross_income < 0 or above_line < 0:
            raise ValueError("income and deductions must be non-negative")

        agi = max(gross_income - above_line, 0.0)
        standard = STANDARD_DEDUCTION[filing_status]
        deduction_used = standard
        deduction_type = "standard"
        if itemized_amount is not None and itemized_amount > standard:
            deduction_used = itemized_amount
            deduction_type = "itemized"

        taxable_income = max(agi - deduction_used, 0.0)
        tax_liability, marginal_rate, breakdown = _compute_tax(
            BRACKETS[filing_status], taxable_income
        )
        effective_rate = tax_liability / gross_income if gross_income > 0 else 0.0

        return {
            "status": "success",
            "data": {
                "agi": agi,
                "taxable_income": taxable_income,
                "tax_liability": tax_liability,
                "effective_rate": effective_rate,
                "marginal_rate": marginal_rate,
                "bracket_breakdown": breakdown,
                "standard_vs_itemized": {
                    "standard_deduction": standard,
                    "itemized_deductions": itemized_amount or 0.0,
                    "deduction_used": deduction_used,
                    "method": deduction_type,
                },
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"federal_income_tax_estimator failed: {e}")
        _log_lesson(f"federal_income_tax_estimator: {e}")
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
