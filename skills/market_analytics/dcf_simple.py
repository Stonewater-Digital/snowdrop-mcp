"""
Execuve Summary: Performs a simplified DCF valuation using forecast FCFs and a terminal growth assumption.
Inputs: free_cash_flows (list[float]), terminal_growth_rate (float), wacc (float)
Outputs: enterprise_value (float), terminal_value (float), terminal_pct_of_ev (float), implied_ev_to_fcf (float), sensitivity_table (dict)
MCP Tool Name: dcf_simple
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "dcf_simple",
    "description": "Discounts forecast free cash flows and a Gordon terminal value to estimate EV.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "free_cash_flows": {"type": "array", "description": "Projected annual FCFs."},
            "terminal_growth_rate": {"type": "number", "description": "Perpetual growth rate after explicit period."},
            "wacc": {"type": "number", "description": "Weighted average cost of capital."}
        },
        "required": ["free_cash_flows", "terminal_growth_rate", "wacc"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def dcf_simple(**kwargs: Any) -> dict:
    """Calculates DCF enterprise value and sensitivity to WACC and growth."""
    try:
        fcfs = kwargs.get("free_cash_flows")
        terminal_growth = kwargs.get("terminal_growth_rate")
        wacc = kwargs.get("wacc")
        if not isinstance(fcfs, list) or len(fcfs) == 0:
            raise ValueError("free_cash_flows must be non-empty list")
        if not isinstance(terminal_growth, (int, float)) or not isinstance(wacc, (int, float)):
            raise ValueError("terminal_growth_rate and wacc must be numeric")
        if wacc <= terminal_growth:
            raise ValueError("wacc must exceed terminal growth rate")

        discounted_fcfs = []
        for year, fcf in enumerate(fcfs, start=1):
            discounted_fcfs.append(float(fcf) / ((1 + wacc) ** year))
        terminal_cash_flow = float(fcfs[-1]) * (1 + terminal_growth)
        terminal_value = terminal_cash_flow / (wacc - terminal_growth)
        terminal_pv = terminal_value / ((1 + wacc) ** len(fcfs))
        enterprise_value = sum(discounted_fcfs) + terminal_pv
        terminal_pct = terminal_pv / enterprise_value if enterprise_value else 0.0
        implied_multiple = enterprise_value / discounted_fcfs[0] if discounted_fcfs[0] else math.inf

        sensitivity_table = {}
        for delta in (-0.01, 0, 0.01):
            g = terminal_growth + delta
            if wacc <= g:
                continue
            tv = float(fcfs[-1]) * (1 + g) / (wacc - g)
            tv_pv = tv / ((1 + wacc) ** len(fcfs))
            sensitivity_table[f"growth_{round(g*100,2)}"] = sum(discounted_fcfs) + tv_pv

        return {
            "status": "success",
            "data": {
                "enterprise_value": enterprise_value,
                "terminal_value": terminal_value,
                "terminal_pct_of_ev": terminal_pct,
                "implied_ev_to_fcf": implied_multiple,
                "sensitivity_table": sensitivity_table
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"dcf_simple failed: {e}")
        _log_lesson(f"dcf_simple: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
