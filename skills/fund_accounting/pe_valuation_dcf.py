"""
Executive Summary: Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate.

Inputs: projected_cashflows (list[float]), discount_rate (float), terminal_growth (float)
Outputs: dict with enterprise_value (float), equity_value (float), implied_multiple (float)
MCP Tool Name: pe_valuation_dcf
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "pe_valuation_dcf",
    "description": "Performs DCF valuation of a private equity investment using projected cash flows, terminal value, and discount rate.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "projected_cashflows": {
                "type": "array",
                "items": {"type": "number"},
                "description": "List of projected annual free cash flows in dollars (year 1 to year N)",
            },
            "discount_rate": {
                "type": "number",
                "description": "Weighted average cost of capital / discount rate (e.g. 0.12 for 12%)",
            },
            "terminal_growth": {
                "type": "number",
                "description": "Terminal growth rate for Gordon Growth Model (e.g. 0.025 for 2.5%)",
            },
            "net_debt": {
                "type": "number",
                "description": "Net debt (debt minus cash) to convert EV to equity value; defaults to 0",
            },
            "total_invested": {
                "type": "number",
                "description": "Total capital invested; used to calculate implied multiple; defaults to 0",
            },
        },
        "required": ["projected_cashflows", "discount_rate", "terminal_growth"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "enterprise_value": {"type": "number"},
            "equity_value": {"type": "number"},
            "implied_multiple": {"type": "number"},
            "terminal_value": {"type": "number"},
            "pv_terminal_value": {"type": "number"},
            "pv_cashflows": {"type": "number"},
            "cashflow_details": {"type": "array"},
            "status": {"type": "string"},
            "timestamp": {"type": "string"},
        },
        "required": [
            "enterprise_value", "equity_value", "implied_multiple",
            "terminal_value", "pv_terminal_value", "pv_cashflows", "status", "timestamp",
        ],
    },
}


def pe_valuation_dcf(
    projected_cashflows: list[float],
    discount_rate: float,
    terminal_growth: float,
    net_debt: float = 0.0,
    total_invested: float = 0.0,
    **kwargs: Any,
) -> dict:
    """Performs a discounted cash flow (DCF) valuation.

    Methodology:
    1. Discount each projected cash flow: PV_t = CF_t / (1 + r)^t
    2. Terminal value (Gordon Growth): TV = last_CF * (1 + g) / (r - g)
    3. PV of terminal value: PV_TV = TV / (1 + r)^N
    4. Enterprise Value = sum(PV_CFs) + PV_TV
    5. Equity Value = EV - net_debt
    6. Implied Multiple = EV / total_invested (if total_invested > 0)

    Args:
        projected_cashflows: List of annual free cash flows (year 1..N).
        discount_rate: WACC or required return rate (e.g. 0.12).
        terminal_growth: Perpetuity growth rate (must be < discount_rate).
        net_debt: Net debt (debt - cash); subtracted from EV to get equity value.
        total_invested: Total capital invested; used to compute implied EV/invested.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Contains enterprise_value, equity_value, implied_multiple,
              terminal_value, pv_terminal_value, pv_cashflows, cashflow_details
              (per-year breakdown), status, timestamp.
    """
    try:
        if not projected_cashflows:
            raise ValueError("projected_cashflows cannot be empty")
        if discount_rate <= 0:
            raise ValueError("discount_rate must be positive")
        if terminal_growth >= discount_rate:
            raise ValueError(
                f"terminal_growth ({terminal_growth}) must be less than discount_rate ({discount_rate})"
            )

        cashflow_details: list[dict] = []
        pv_cashflows = 0.0

        for t, cf in enumerate(projected_cashflows, start=1):
            discount_factor = (1.0 + discount_rate) ** t
            pv = cf / discount_factor
            pv_cashflows += pv
            cashflow_details.append({
                "year": t,
                "cashflow": round(cf, 2),
                "discount_factor": round(discount_factor, 6),
                "present_value": round(pv, 2),
            })

        last_cf = float(projected_cashflows[-1])
        n = len(projected_cashflows)

        # Gordon Growth Model terminal value at end of projection period
        terminal_value = last_cf * (1.0 + terminal_growth) / (discount_rate - terminal_growth)
        pv_terminal_value = terminal_value / ((1.0 + discount_rate) ** n)

        enterprise_value = pv_cashflows + pv_terminal_value
        equity_value = enterprise_value - net_debt

        implied_multiple = enterprise_value / total_invested if total_invested > 0 else 0.0

        tv_pct_of_ev = pv_terminal_value / enterprise_value if enterprise_value != 0 else 0.0

        result = {
            "enterprise_value": round(enterprise_value, 2),
            "equity_value": round(equity_value, 2),
            "implied_multiple": round(implied_multiple, 4),
            "terminal_value": round(terminal_value, 2),
            "pv_terminal_value": round(pv_terminal_value, 2),
            "pv_cashflows": round(pv_cashflows, 2),
            "terminal_value_pct_of_ev": round(tv_pct_of_ev, 4),
            "discount_rate": discount_rate,
            "terminal_growth_rate": terminal_growth,
            "net_debt": round(net_debt, 2),
            "total_invested": round(total_invested, 2),
            "projection_years": n,
            "cashflow_details": cashflow_details,
        }
        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        logger.error(f"pe_valuation_dcf failed: {e}")
        _log_lesson(f"pe_valuation_dcf: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Appends an error lesson to the lessons log.

    Args:
        message: The lesson message to log.
    """
    os.makedirs("logs", exist_ok=True)
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
