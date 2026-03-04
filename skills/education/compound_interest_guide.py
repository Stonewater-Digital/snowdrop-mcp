"""Educational guide to compound interest and the power of compounding.

MCP Tool Name: compound_interest_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "compound_interest_guide",
    "description": "Returns educational content on compound interest: formula, Rule of 72, compounding frequencies, and examples.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def compound_interest_guide() -> dict[str, Any]:
    """Returns educational content on compound interest."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Compound interest is interest calculated on both the initial principal and the accumulated interest from previous periods. It is often called 'interest on interest' and is the primary mechanism through which investments grow exponentially over time.",
                "key_concepts": [
                    "Compound interest grows exponentially, not linearly",
                    "Time is the most powerful factor — starting early matters more than investing more later",
                    "More frequent compounding produces higher effective returns",
                    "Albert Einstein reportedly called compound interest the eighth wonder of the world",
                ],
                "formula": "A = P(1 + r/n)^(n*t), where A = final amount, P = principal, r = annual interest rate (decimal), n = compounding frequency per year, t = number of years",
                "compounding_frequencies": {
                    "annual": "n = 1. Interest compounds once per year. $10,000 at 8% for 10 years = $21,589.",
                    "semi_annual": "n = 2. Interest compounds twice per year. $10,000 at 8% for 10 years = $21,911.",
                    "quarterly": "n = 4. Interest compounds four times per year. $10,000 at 8% for 10 years = $22,080.",
                    "monthly": "n = 12. Interest compounds twelve times per year. $10,000 at 8% for 10 years = $22,196.",
                    "daily": "n = 365. Interest compounds every day. $10,000 at 8% for 10 years = $22,253.",
                    "continuous": "Formula: A = Pe^(r*t). The theoretical limit. $10,000 at 8% for 10 years = $22,255.",
                },
                "rule_of_72": {
                    "definition": "A quick mental math shortcut to estimate how long it takes for an investment to double in value.",
                    "formula": "Years to double = 72 / annual interest rate",
                    "examples": [
                        "At 6% return: 72 / 6 = 12 years to double",
                        "At 8% return: 72 / 8 = 9 years to double",
                        "At 10% return: 72 / 10 = 7.2 years to double",
                        "At 12% return: 72 / 12 = 6 years to double",
                    ],
                    "accuracy": "Most accurate for rates between 6-10%. For other rates, use 69.3 (the natural log version) or 70 for easier mental math.",
                },
                "example": {
                    "scenario": "Investor A starts at age 25, investing $5,000/year for 10 years (total invested: $50,000), then stops contributing. Investor B starts at age 35, investing $5,000/year for 30 years (total invested: $150,000). Both earn 8% annually.",
                    "result_A": "Investor A at age 65: approximately $787,000 (invested only $50,000).",
                    "result_B": "Investor B at age 65: approximately $611,000 (invested $150,000).",
                    "lesson": "Despite investing three times less money, Investor A ends up with more because of 10 extra years of compounding.",
                },
                "simple_vs_compound": {
                    "simple_interest": "Calculated only on the original principal. Formula: A = P(1 + r*t). $10,000 at 8% for 10 years = $18,000.",
                    "compound_interest": "$10,000 at 8% compounded annually for 10 years = $21,589.",
                    "difference": "The $3,589 difference is entirely from earning interest on accumulated interest.",
                },
                "common_mistakes": [
                    "Underestimating the impact of starting early — even a few years make a significant difference",
                    "Ignoring the negative compounding of debt (credit card interest compounds against you)",
                    "Forgetting that fees and taxes also compound, eroding returns over time",
                    "Confusing nominal rate with effective annual rate when compounding is more frequent",
                    "Withdrawing from investments and breaking the compounding chain",
                ],
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
