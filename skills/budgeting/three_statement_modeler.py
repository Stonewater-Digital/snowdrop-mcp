"""Link income statement, balance sheet, and cash flow projections."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "three_statement_modeler",
    "description": "Generates linked financial statements using indirect cash flow method.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "income_statement": {"type": "object"},
            "prior_balance_sheet": {"type": "object"},
            "assumptions": {"type": "object"},
        },
        "required": ["income_statement", "prior_balance_sheet", "assumptions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {"type": "object"},
            "timestamp": {"type": "string"},
        },
    },
}


def three_statement_modeler(
    income_statement: dict[str, Any],
    prior_balance_sheet: dict[str, Any],
    assumptions: dict[str, Any],
    **_: Any,
) -> dict[str, Any]:
    """Build linked financial statements and confirm the balance sheet balances."""
    try:
        revenue = float(income_statement.get("revenue", 0.0))
        cogs = float(income_statement.get("cogs", 0.0))
        operating_expenses = float(income_statement.get("operating_expenses", 0.0))
        interest = float(income_statement.get("interest", 0.0))
        tax_rate = float(income_statement.get("tax_rate", 0.0))

        gross_profit = revenue - cogs
        ebit = gross_profit - operating_expenses
        taxable_income = ebit - interest
        taxes = max(taxable_income, 0) * tax_rate
        net_income = taxable_income - taxes

        days_receivable = int(assumptions.get("days_receivable", 30))
        days_payable = int(assumptions.get("days_payable", 30))
        capex = float(assumptions.get("capex", 0.0))
        debt_repayment = float(assumptions.get("debt_repayment", 0.0))

        receivables = revenue / 30 * days_receivable
        payables = cogs / 30 * days_payable
        prior_cash = float(prior_balance_sheet.get("cash", 0.0))
        prior_receivables = float(prior_balance_sheet.get("receivables", 0.0))
        prior_payables = float(prior_balance_sheet.get("payables", 0.0))
        prior_debt = float(prior_balance_sheet.get("debt", 0.0))
        prior_equity = float(prior_balance_sheet.get("equity", 0.0))

        change_receivables = receivables - prior_receivables
        change_payables = payables - prior_payables
        operating_cash_flow = net_income + (change_payables - change_receivables)
        investing_cash_flow = -capex
        financing_cash_flow = -(debt_repayment)
        net_cash_flow = operating_cash_flow + investing_cash_flow + financing_cash_flow
        ending_cash = prior_cash + net_cash_flow

        ending_debt = max(prior_debt - debt_repayment, 0)
        retained_earnings = prior_equity + net_income
        total_assets = ending_cash + receivables + float(prior_balance_sheet.get("other_assets", 0.0))
        total_liabilities = ending_debt + payables
        total_equity = retained_earnings
        balanced = round(total_assets, 2) == round(total_liabilities + total_equity, 2)

        statements = {
            "income_statement": {
                "revenue": revenue,
                "cogs": cogs,
                "gross_profit": gross_profit,
                "operating_expenses": operating_expenses,
                "ebit": ebit,
                "interest": interest,
                "taxes": taxes,
                "net_income": net_income,
            },
            "cash_flow": {
                "operating": round(operating_cash_flow, 2),
                "investing": round(investing_cash_flow, 2),
                "financing": round(financing_cash_flow, 2),
                "net_change": round(net_cash_flow, 2),
            },
            "balance_sheet": {
                "cash": round(ending_cash, 2),
                "receivables": round(receivables, 2),
                "payables": round(payables, 2),
                "debt": round(ending_debt, 2),
                "equity": round(retained_earnings, 2),
                "assets": round(total_assets, 2),
                "liabilities_plus_equity": round(total_liabilities + total_equity, 2),
            },
            "balanced": balanced,
        }
        return {
            "status": "success",
            "data": statements,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("three_statement_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
