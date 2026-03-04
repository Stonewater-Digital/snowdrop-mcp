"""
Executive Smary: Compares annuitized pension payments versus a lump sum offer using PV math.
Inputs: monthly_pension (float), lump_sum_offer (float), life_expectancy_years (float), discount_rate (float), inflation_rate (float), tax_bracket (float)
Outputs: pension_pv (float), lump_sum_after_tax (float), breakeven_years (float), recommended_choice (str), sensitivity_table (list)
MCP Tool Name: pension_vs_lump_sum
"""
import logging
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "pension_vs_lump_sum",
    "description": (
        "Values lifetime pension payments versus a lump sum using discounting and "
        "inflation adjustments, providing breakeven timing and sensitivity scenarios."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_pension": {
                "type": "number",
                "description": "Guaranteed monthly pension payment before taxes.",
            },
            "lump_sum_offer": {
                "type": "number",
                "description": "One-time buyout offer for the pension.",
            },
            "life_expectancy_years": {
                "type": "number",
                "description": "Expected years of benefit payments.",
            },
            "discount_rate": {
                "type": "number",
                "description": "Annual discount rate to present value the annuity.",
            },
            "inflation_rate": {
                "type": "number",
                "description": "Expected inflation to adjust the real discount rate.",
            },
            "tax_bracket": {
                "type": "number",
                "description": "Marginal tax rate applied to lump sum and pension.",
            },
        },
        "required": [
            "monthly_pension",
            "lump_sum_offer",
            "life_expectancy_years",
            "discount_rate",
            "inflation_rate",
            "tax_bracket",
        ],
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


def pension_vs_lump_sum(**kwargs: Any) -> dict:
    """Value pension annuity vs. lump sum using present value comparisons."""
    try:
        monthly_pension = float(kwargs["monthly_pension"])
        lump_sum_offer = float(kwargs["lump_sum_offer"])
        life_expectancy = float(kwargs["life_expectancy_years"])
        discount_rate = float(kwargs["discount_rate"])
        inflation_rate = float(kwargs["inflation_rate"])
        tax_bracket = float(kwargs["tax_bracket"])

        if monthly_pension < 0 or lump_sum_offer < 0 or life_expectancy <= 0:
            raise ValueError("pension, lump sum, and life expectancy must be positive")

        real_discount = (1 + discount_rate) / (1 + inflation_rate) - 1
        annuity_rate = real_discount if real_discount != 0 else 1e-9
        pension_pv = (
            monthly_pension
            * 12
            * (1 - (1 + annuity_rate) ** (-life_expectancy))
            / annuity_rate
            * (1 - tax_bracket)
        )
        lump_sum_after_tax = lump_sum_offer * (1 - tax_bracket)
        breakeven_years = (
            lump_sum_after_tax / (monthly_pension * 12 * (1 - tax_bracket))
            if monthly_pension > 0
            else 0
        )
        recommended_choice = "pension" if pension_pv > lump_sum_after_tax else "lump_sum"
        sensitivity_table = []
        for dr_shift in (-0.01, 0, 0.01):
            for life_shift in (-2, 0, 2):
                adj_discount = max(real_discount + dr_shift, 0.0001)
                adj_life = max(life_expectancy + life_shift, 1)
                adj_pv = (
                    monthly_pension
                    * 12
                    * (1 - (1 + adj_discount) ** (-adj_life))
                    / adj_discount
                    * (1 - tax_bracket)
                )
                sensitivity_table.append(
                    {
                        "discount_rate": real_discount + dr_shift,
                        "life_expectancy_years": adj_life,
                        "pension_pv": adj_pv,
                    }
                )

        return {
            "status": "success",
            "data": {
                "pension_pv": pension_pv,
                "lump_sum_after_tax": lump_sum_after_tax,
                "breakeven_years": breakeven_years,
                "recommended_choice": recommended_choice,
                "sensitivity_table": sensitivity_table,
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"pension_vs_lump_sum failed: {e}")
        _log_lesson(f"pension_vs_lump_sum: {e}")
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
