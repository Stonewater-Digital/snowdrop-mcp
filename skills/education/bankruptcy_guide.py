"""Educational guide to bankruptcy fundamentals.

MCP Tool Name: bankruptcy_guide
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "bankruptcy_guide",
    "description": "Returns educational content on bankruptcy: Chapter 7 vs 11 vs 13, process, effects, and alternatives.",
    "inputSchema": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def bankruptcy_guide() -> dict[str, Any]:
    """Returns educational content on bankruptcy."""
    try:
        return {
            "status": "ok",
            "data": {
                "definition": "Bankruptcy is a legal process under federal law that provides debt relief to individuals and businesses who cannot pay their debts. It either liquidates assets to pay creditors (Chapter 7) or creates a court-approved repayment plan (Chapter 11 or 13). The goal is a fresh financial start for the debtor while providing fair treatment to creditors.",
                "key_concepts": [
                    "Bankruptcy is a federal legal proceeding handled by specialized bankruptcy courts",
                    "Filing triggers an automatic stay — creditors must stop all collection actions",
                    "Not all debts can be discharged (student loans, taxes, child support are typically non-dischargeable)",
                    "Bankruptcy remains on credit reports for 7-10 years",
                ],
                "chapters": {
                    "chapter_7": {
                        "name": "Chapter 7 — Liquidation",
                        "who": "Individuals and businesses with limited income who cannot repay debts. Must pass a means test (income below state median or disposable income below threshold).",
                        "process": "A court-appointed trustee liquidates non-exempt assets to pay creditors. Many assets are exempt (home equity up to a limit, car, personal property, retirement accounts).",
                        "timeline": "Typically 3-6 months from filing to discharge.",
                        "result": "Most unsecured debts (credit cards, medical bills) are eliminated. Secured debts require returning the collateral or continuing payments.",
                        "credit_impact": "Stays on credit report for 10 years.",
                    },
                    "chapter_11": {
                        "name": "Chapter 11 — Reorganization",
                        "who": "Primarily businesses (but available to individuals with large debts). Allows continued operation while restructuring debts.",
                        "process": "The debtor proposes a reorganization plan to restructure debts, renegotiate contracts, and return to profitability. Creditors vote on the plan. The court must approve it.",
                        "timeline": "Can take 6 months to several years depending on complexity.",
                        "result": "The business continues operating under a court-approved plan. Debts may be reduced, extended, or converted. Equity holders often lose most or all value.",
                        "credit_impact": "Stays on credit report for 7-10 years.",
                    },
                    "chapter_13": {
                        "name": "Chapter 13 — Wage Earner's Plan",
                        "who": "Individuals with regular income who want to keep their property (home, car) and repay debts over time. Debt limits apply.",
                        "process": "The debtor proposes a 3-5 year repayment plan using future income. Unsecured creditors receive a percentage of what they are owed.",
                        "timeline": "Repayment plan lasts 3-5 years. Discharge occurs upon completion.",
                        "result": "Debtor keeps all property. Pays back some portion of debts. Remaining qualifying debts discharged after plan completion.",
                        "credit_impact": "Stays on credit report for 7 years.",
                    },
                },
                "effects": {
                    "on_credit": "Severe negative impact. Score typically drops 130-200+ points. Difficulty obtaining new credit for 2-4 years. Higher interest rates for years after.",
                    "on_assets": "Chapter 7 may require liquidating non-exempt assets. Chapter 13 allows keeping all assets. Retirement accounts (401k, IRA) are generally protected in all chapters.",
                    "on_employment": "Some employers check credit for certain positions (financial sector). Bankruptcy cannot be the sole reason for termination but may affect job prospects.",
                    "on_housing": "Difficulty renting for 2-3 years after filing. Many landlords check credit. Mortgage approval difficult for 2-4 years (FHA: 2 years, conventional: 4 years).",
                },
                "alternatives": [
                    "Debt consolidation — combine multiple debts into one lower-rate loan",
                    "Debt management plan — work with a nonprofit credit counselor to negotiate lower rates and a repayment plan",
                    "Debt settlement — negotiate with creditors to accept less than the full amount owed (typically 40-60 cents on the dollar)",
                    "Balance transfer — move high-interest credit card debt to a 0% APR promotional card",
                    "Hardship programs — contact creditors directly to request reduced payments, lower rates, or forbearance",
                    "Sell assets voluntarily — may be better than forced liquidation",
                ],
                "example": "A family with $80,000 in credit card debt, $30,000 in medical bills, and $50,000 household income qualifies for Chapter 7 (below state median income). After filing, the automatic stay stops creditor calls and lawsuits. Their exempt home, car, and retirement accounts are protected. After 4 months, $110,000 in unsecured debt is discharged.",
                "common_mistakes": [
                    "Waiting too long to file — emptying retirement accounts or running up more debt before seeking help",
                    "Assuming bankruptcy discharges all debts (student loans, recent taxes, and child support are typically non-dischargeable)",
                    "Filing without exploring alternatives that may be less damaging to credit",
                    "Not understanding the difference between chapters and filing under the wrong one",
                    "Transferring assets or paying preferred creditors before filing (can be reversed by the trustee as fraudulent transfers)",
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
