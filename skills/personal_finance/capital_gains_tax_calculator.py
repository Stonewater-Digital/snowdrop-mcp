"""
Executive Smary: Calculates federal tax on short- and long-term capital gains with NIIT.
Inputs: gains (list), ordinary_income (float), filing_status (str)
Outputs: short_term_gains (float), long_term_gains (float), st_tax (float), lt_tax (float), total_tax (float), effective_rate (float), niit_applicability (dict)
MCP Tool Name: capital_gains_tax_calculator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List, Tuple

logger = logging.getLogger("snowdrop.skills")

ORDINARY_BRACKETS = {
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

LONG_TERM_BRACKETS = {
    "single": [(0, 0.0), (47025, 0.15), (518900, 0.20)],
    "mfj": [(0, 0.0), (94050, 0.15), (583750, 0.20)],
}

NIIT_THRESHOLDS = {"single": 200000, "mfj": 250000}


def _marginal_tax(brackets: List[Tuple[float, float]], income: float) -> float:
    tax = 0.0
    for idx, (threshold, rate) in enumerate(brackets):
        next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
        if income <= threshold:
            break
        upper = next_threshold if next_threshold is not None else income
        amount = min(income, upper) - threshold
        if amount <= 0:
            continue
        tax += amount * rate
    return tax


TOOL_META = {
    "name": "capital_gains_tax_calculator",
    "description": (
        "Splits gains into short- and long-term buckets, applies 2024 tax brackets, and "
        "checks 3.8% NIIT applicability based on filing status and income."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "gains": {
                "type": "array",
                "description": "List of realized transactions with amount, holding_period_months, cost_basis.",
                "items": {"type": "object"},
            },
            "ordinary_income": {
                "type": "number",
                "description": "Other taxable ordinary income in dollars.",
            },
            "filing_status": {
                "type": "string",
                "description": "single or mfj for capital gains thresholds.",
            },
        },
        "required": ["gains", "ordinary_income", "filing_status"],
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


def capital_gains_tax_calculator(**kwargs: Any) -> dict:
    """Compute capital gains tax for 2024 including NIIT if applicable."""
    try:
        gains_input = kwargs["gains"]
        ordinary_income = float(kwargs["ordinary_income"])
        filing_status = str(kwargs["filing_status"]).strip().lower()

        if filing_status not in ORDINARY_BRACKETS:
            raise ValueError("filing_status must be single or mfj")
        if not isinstance(gains_input, list):
            raise ValueError("gains must be a list")

        short_term = 0.0
        long_term = 0.0
        for tx in gains_input:
            amount = float(tx["amount"])
            holding_months = int(tx["holding_period_months"])
            if holding_months < 12:
                short_term += amount
            else:
                long_term += amount

        # Short-term taxed as ordinary income
        baseline_tax = _marginal_tax(ORDINARY_BRACKETS[filing_status], max(ordinary_income, 0.0))
        combined_tax = _marginal_tax(
            ORDINARY_BRACKETS[filing_status], max(ordinary_income + short_term, 0.0)
        )
        st_tax = combined_tax - baseline_tax

        # Long-term rates
        lt_tax = 0.0
        remaining = long_term
        brackets = LONG_TERM_BRACKETS[filing_status]
        taxable_base = ordinary_income + short_term
        for idx, (threshold, rate) in enumerate(brackets):
            next_threshold = brackets[idx + 1][0] if idx + 1 < len(brackets) else None
            room = (
                (next_threshold - taxable_base) if next_threshold is not None else remaining
            )
            amount = min(max(room, 0.0), remaining)
            if amount <= 0:
                continue
            lt_tax += amount * rate
            remaining -= amount
            taxable_base += amount
            if remaining <= 0:
                break
        if remaining > 0:
            lt_tax += remaining * brackets[-1][1]

        total_gains = short_term + long_term
        total_tax = st_tax + lt_tax

        # NIIT
        threshold = NIIT_THRESHOLDS[filing_status]
        magi = ordinary_income + total_gains
        niit_tax = 0.0
        applies = magi > threshold
        if applies:
            niit_tax = 0.038 * min(total_gains, magi - threshold)
            total_tax += niit_tax

        effective_rate = total_tax / total_gains if total_gains > 0 else 0.0

        return {
            "status": "success",
            "data": {
                "short_term_gains": short_term,
                "long_term_gains": long_term,
                "st_tax": st_tax,
                "lt_tax": lt_tax,
                "total_tax": total_tax,
                "effective_rate": effective_rate,
                "niit_applicability": {"applies": applies, "niit_tax": niit_tax},
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"capital_gains_tax_calculator failed: {e}")
        _log_lesson(f"capital_gains_tax_calculator: {e}")
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
