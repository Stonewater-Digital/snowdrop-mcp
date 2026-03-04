"""Compare the 5-year cost of renting vs buying a home.

MCP Tool Name: rent_vs_buy_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "rent_vs_buy_calculator",
    "description": "Compare 5-year total cost of renting vs buying. Accounts for mortgage payments, property tax, insurance, maintenance, appreciation, equity buildup, and rent increases.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "monthly_rent": {
                "type": "number",
                "description": "Current monthly rent in USD.",
            },
            "home_price": {
                "type": "number",
                "description": "Home purchase price in USD.",
            },
            "down_payment_pct": {
                "type": "number",
                "description": "Down payment as a decimal (e.g. 0.20 for 20%).",
                "default": 0.20,
            },
            "mortgage_rate": {
                "type": "number",
                "description": "Annual mortgage interest rate as a decimal.",
                "default": 0.07,
            },
            "term_years": {
                "type": "integer",
                "description": "Mortgage term in years.",
                "default": 30,
            },
            "annual_appreciation": {
                "type": "number",
                "description": "Expected annual home appreciation rate as a decimal.",
                "default": 0.03,
            },
        },
        "required": ["monthly_rent", "home_price"],
    },
}

_PROPERTY_TAX_RATE = 0.012  # 1.2% of home value
_INSURANCE_RATE = 0.005     # 0.5% of home value
_MAINTENANCE_RATE = 0.01    # 1% of home value
_RENT_INCREASE_RATE = 0.03  # 3% annual rent increase
_ANALYSIS_YEARS = 5


def rent_vs_buy_calculator(
    monthly_rent: float,
    home_price: float,
    down_payment_pct: float = 0.20,
    mortgage_rate: float = 0.07,
    term_years: int = 30,
    annual_appreciation: float = 0.03,
) -> dict[str, Any]:
    """Compare 5-year cost of renting vs buying."""
    try:
        if home_price <= 0 or monthly_rent < 0:
            return {
                "status": "error",
                "data": {"error": "home_price must be positive and monthly_rent non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        down_payment = home_price * down_payment_pct
        loan_amount = home_price - down_payment

        # Monthly mortgage payment
        monthly_rate = mortgage_rate / 12
        n_payments = term_years * 12
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate) ** n_payments) / ((1 + monthly_rate) ** n_payments - 1)
        else:
            monthly_payment = loan_amount / n_payments

        # 5-year rent cost
        total_rent = 0.0
        current_rent = monthly_rent
        for year in range(_ANALYSIS_YEARS):
            total_rent += current_rent * 12
            current_rent *= (1 + _RENT_INCREASE_RATE)

        # 5-year ownership cost
        total_mortgage = monthly_payment * 12 * _ANALYSIS_YEARS

        # Calculate equity buildup (principal paid over 5 years)
        balance = loan_amount
        total_interest = 0.0
        total_principal_paid = 0.0
        for _ in range(_ANALYSIS_YEARS * 12):
            interest_payment = balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            total_interest += interest_payment
            total_principal_paid += principal_payment
            balance -= principal_payment

        # Other ownership costs over 5 years
        total_property_tax = 0.0
        total_insurance = 0.0
        total_maintenance = 0.0
        current_value = home_price
        for year in range(_ANALYSIS_YEARS):
            total_property_tax += current_value * _PROPERTY_TAX_RATE
            total_insurance += current_value * _INSURANCE_RATE
            total_maintenance += current_value * _MAINTENANCE_RATE
            current_value *= (1 + annual_appreciation)

        # Home value after 5 years
        home_value_5yr = home_price * (1 + annual_appreciation) ** _ANALYSIS_YEARS
        appreciation_gain = home_value_5yr - home_price
        equity_at_5yr = down_payment + total_principal_paid + appreciation_gain

        total_ownership_cost = total_mortgage + total_property_tax + total_insurance + total_maintenance + down_payment
        net_ownership_cost = total_ownership_cost - equity_at_5yr

        recommendation = "buy" if net_ownership_cost < total_rent else "rent"

        return {
            "status": "ok",
            "data": {
                "analysis_period_years": _ANALYSIS_YEARS,
                "rent": {
                    "starting_monthly_rent": round(monthly_rent, 2),
                    "annual_rent_increase_pct": round(_RENT_INCREASE_RATE * 100, 1),
                    "total_5yr_rent": round(total_rent, 2),
                },
                "buy": {
                    "home_price": round(home_price, 2),
                    "down_payment": round(down_payment, 2),
                    "loan_amount": round(loan_amount, 2),
                    "monthly_mortgage": round(monthly_payment, 2),
                    "mortgage_rate_pct": round(mortgage_rate * 100, 2),
                    "total_mortgage_payments": round(total_mortgage, 2),
                    "total_interest_5yr": round(total_interest, 2),
                    "total_principal_paid_5yr": round(total_principal_paid, 2),
                    "total_property_tax_5yr": round(total_property_tax, 2),
                    "total_insurance_5yr": round(total_insurance, 2),
                    "total_maintenance_5yr": round(total_maintenance, 2),
                    "home_value_at_5yr": round(home_value_5yr, 2),
                    "appreciation_gain": round(appreciation_gain, 2),
                    "equity_at_5yr": round(equity_at_5yr, 2),
                    "total_ownership_cost": round(total_ownership_cost, 2),
                    "net_ownership_cost": round(net_ownership_cost, 2),
                },
                "recommendation": recommendation,
                "savings_over_5yr": round(abs(total_rent - net_ownership_cost), 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
