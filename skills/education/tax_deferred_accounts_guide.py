"""Educational guide to tax-deferred and tax-advantaged retirement accounts.

MCP Tool Name: tax_deferred_accounts_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "tax_deferred_accounts_guide",
    "description": "Returns educational content on tax-advantaged accounts: 401(k), IRA, Roth, HSA, contribution limits, and RMDs.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def tax_deferred_accounts_guide() -> dict[str, Any]:
    """Returns educational content on tax-deferred accounts."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Tax-deferred and tax-advantaged accounts are special account types created by Congress to incentivize retirement saving and healthcare spending. They provide tax benefits — either upfront deductions, tax-free growth, or tax-free withdrawals — that significantly increase long-term wealth accumulation compared to taxable accounts.",
                "key_concepts": [
                    "Tax-deferred means you pay taxes later (traditional 401k/IRA). Tax-free means you never pay taxes on growth (Roth).",
                    "The right account depends on your current vs expected future tax rate",
                    "Contribution limits are set by the IRS and adjusted periodically for inflation",
                    "Early withdrawals before age 59.5 generally incur a 10% penalty plus taxes",
                ],
                "account_types": {
                    "traditional_401k": {
                        "description": "Employer-sponsored retirement plan. Contributions are pre-tax (reduce taxable income). Investments grow tax-deferred. Withdrawals in retirement are taxed as ordinary income.",
                        "contribution_limit_2025": "$23,500 ($31,000 if age 50+, catch-up contribution of $7,500)",
                        "employer_match": "Many employers match contributions up to 3-6% of salary. This is free money — always contribute enough to get the full match.",
                        "tax_benefit": "Immediate tax deduction. A $10,000 contribution at 24% tax bracket saves $2,400 in current-year taxes.",
                        "rmd": "Required Minimum Distributions start at age 73 (SECURE 2.0 Act). Must withdraw a minimum amount annually.",
                    },
                    "roth_401k": {
                        "description": "Same employer-sponsored plan but contributions are after-tax. No upfront deduction. Qualified withdrawals in retirement are completely tax-free.",
                        "contribution_limit_2025": "Same as traditional 401k — $23,500 ($31,000 if 50+). Combined limit with traditional.",
                        "best_for": "Young workers expecting higher future tax rates. No income limits for contributions (unlike Roth IRA).",
                        "rmd": "Starting in 2024 (SECURE 2.0), Roth 401k is no longer subject to RMDs. Previously required rolling to Roth IRA to avoid RMDs.",
                    },
                    "traditional_ira": {
                        "description": "Individual Retirement Account. Contributions may be tax-deductible depending on income and whether you have an employer plan. Growth is tax-deferred. Withdrawals taxed as ordinary income.",
                        "contribution_limit_2025": "$7,000 ($8,000 if age 50+)",
                        "deductibility": "Fully deductible if no employer plan. Phase-out applies if covered by employer plan (single: $79,000-$89,000 MAGI; married: $126,000-$146,000).",
                        "rmd": "Required starting at age 73.",
                    },
                    "roth_ira": {
                        "description": "Individual Retirement Account with after-tax contributions. No upfront deduction. Qualified withdrawals are completely tax-free (contributions and earnings). No RMDs during the owner's lifetime.",
                        "contribution_limit_2025": "$7,000 ($8,000 if age 50+). Same combined limit with traditional IRA.",
                        "income_limits_2025": "Phase-out: single $150,000-$165,000 MAGI; married filing jointly $236,000-$246,000.",
                        "backdoor_roth": "High earners can contribute to a traditional IRA (non-deductible) and convert to Roth. Must consider pro-rata rule if you have other traditional IRA balances.",
                        "best_for": "Young workers, those expecting higher future tax rates, those wanting tax-free retirement income with no RMDs.",
                    },
                    "hsa": {
                        "description": "Health Savings Account. Triple tax advantage: contributions are tax-deductible, growth is tax-free, and withdrawals for qualified medical expenses are tax-free. Requires a High-Deductible Health Plan (HDHP).",
                        "contribution_limit_2025": "$4,300 individual / $8,550 family ($1,000 catch-up if 55+)",
                        "triple_tax_benefit": "No other account offers all three tax advantages. Often called the best retirement account in the tax code.",
                        "investment_strategy": "Pay current medical expenses out-of-pocket if possible, invest HSA funds for long-term growth, and withdraw tax-free for medical expenses in retirement.",
                        "after_65": "After age 65, HSA withdrawals for non-medical expenses are taxed as ordinary income (like a traditional IRA) but without penalty.",
                    },
                },
                "contribution_limits_summary_2025": {
                    "401k_under_50": "$23,500",
                    "401k_50_plus": "$31,000",
                    "ira_under_50": "$7,000",
                    "ira_50_plus": "$8,000",
                    "hsa_individual": "$4,300",
                    "hsa_family": "$8,550",
                    "note": "Limits are adjusted periodically for inflation. Always verify current year limits with the IRS.",
                },
                "rmds": {
                    "definition": "Required Minimum Distributions are mandatory annual withdrawals from tax-deferred accounts starting at age 73 (as of SECURE 2.0 Act).",
                    "calculation": "RMD = Account Balance (Dec 31 of prior year) / IRS Life Expectancy Factor. The factor decreases with age, so withdrawals increase.",
                    "applies_to": "Traditional 401k, traditional IRA, SEP IRA, SIMPLE IRA. Does NOT apply to Roth IRA during the owner's lifetime.",
                    "penalty_for_missing": "25% excise tax on the amount not withdrawn (reduced from 50%). Can be reduced to 10% if corrected within 2 years.",
                },
                "example": "A 30-year-old earning $80,000 contributes $10,000/year to a Roth 401k. At 8% annual return over 35 years, the account grows to approximately $1.86 million — all of which can be withdrawn completely tax-free in retirement. The same amount in a traditional 401k at a 22% tax rate in retirement would net approximately $1.45 million after taxes.",
                "common_mistakes": [
                    "Not contributing enough to get the full employer match (leaving free money on the table)",
                    "Choosing Roth vs Traditional without considering current and future tax rates",
                    "Cashing out retirement accounts when changing jobs instead of rolling over",
                    "Ignoring the HSA as a retirement savings vehicle — treating it only as a spending account",
                    "Not aware of RMD requirements and incurring the 25% penalty",
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
