"""Educational guide to credit scores and credit management.

MCP Tool Name: credit_score_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "credit_score_guide",
    "description": "Returns educational content on credit scores: FICO ranges, scoring factors, and improvement tips.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def credit_score_guide() -> dict[str, Any]:
    """Returns educational content on credit scores."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "A credit score is a numerical representation (typically 300-850) of a person's creditworthiness, based on their credit history. Lenders use it to assess the risk of lending money. The most widely used scoring model is FICO, developed by Fair Isaac Corporation.",
                "key_concepts": [
                    "Credit scores affect interest rates, loan approval, and even employment and housing decisions",
                    "Multiple scoring models exist (FICO, VantageScore) with slightly different methodologies",
                    "You have multiple credit scores — each bureau (Equifax, Experian, TransUnion) may have different data",
                    "Credit scores change over time based on your financial behavior",
                ],
                "fico_ranges": {
                    "exceptional": {"range": "800-850", "description": "Well above average. Qualifies for the best rates and terms. Demonstrates a long history of responsible credit management."},
                    "very_good": {"range": "740-799", "description": "Above average. Qualifies for excellent rates. Demonstrates dependable credit behavior."},
                    "good": {"range": "670-739", "description": "Near or slightly above average. Most lenders consider this acceptable. May not get the very best rates."},
                    "fair": {"range": "580-669", "description": "Below average. Some lenders will approve with higher interest rates. Subprime borrower territory."},
                    "poor": {"range": "300-579", "description": "Well below average. Difficulty getting approved. May require secured cards or co-signers. Very high interest rates if approved."},
                },
                "scoring_factors": {
                    "payment_history": {
                        "weight": "35%",
                        "description": "The most important factor. Whether you pay bills on time. Late payments, collections, and bankruptcies have the largest negative impact. A single 30-day late payment can drop a score 60-100+ points.",
                    },
                    "credit_utilization": {
                        "weight": "30%",
                        "description": "The ratio of credit card balances to credit limits. Lower is better. Keep below 30%, ideally below 10%. Calculated per card and across all cards. High utilization signals over-reliance on credit.",
                    },
                    "length_of_credit_history": {
                        "weight": "15%",
                        "description": "Average age of all accounts and age of oldest account. Longer history is better. This is why closing old accounts can hurt your score. Opening many new accounts lowers the average age.",
                    },
                    "credit_mix": {
                        "weight": "10%",
                        "description": "Having a variety of credit types: credit cards (revolving), mortgage, auto loan, student loan (installment). A healthy mix shows you can manage different types of credit responsibly.",
                    },
                    "new_credit_inquiries": {
                        "weight": "10%",
                        "description": "Hard inquiries from new credit applications. Each inquiry may lower your score by 5-10 points. Multiple inquiries for the same loan type within 14-45 days count as one (rate shopping window).",
                    },
                },
                "improvement_tips": [
                    "Pay all bills on time, every time — set up autopay for at least the minimum payment",
                    "Reduce credit card balances below 30% of limits (below 10% for maximum impact)",
                    "Do not close old credit card accounts — keep them open for length of history",
                    "Limit new credit applications — only apply when necessary",
                    "Check your credit reports annually for errors and dispute inaccuracies (AnnualCreditReport.com)",
                    "Become an authorized user on a family member's old, low-utilization card",
                    "Consider a secured credit card if building credit from scratch",
                    "Avoid collections at all costs — negotiate payment plans before accounts go to collections",
                    "Diversify credit types over time (but do not take on unnecessary debt)",
                    "Be patient — negative items fall off after 7 years (10 years for bankruptcy)",
                ],
                "example": "A person with a 680 FICO score applies for a mortgage. They qualify at 6.5% on a $300,000 30-year loan ($1,896/month). If they improve to 740, the rate drops to 5.8% ($1,759/month), saving $137/month or $49,320 over the life of the loan.",
                "common_mistakes": [
                    "Closing old credit cards to 'clean up' — this shortens credit history and increases utilization",
                    "Paying only the minimum on credit cards — balances barely decrease due to interest",
                    "Applying for multiple credit cards in a short period (many hard inquiries)",
                    "Ignoring credit reports — errors are common and can significantly hurt your score",
                    "Maxing out credit cards even if you pay in full monthly (utilization is reported at statement date)",
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
