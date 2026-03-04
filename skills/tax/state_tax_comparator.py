"""Compare effective state income tax rates across states.

MCP Tool Name: state_tax_comparator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "state_tax_comparator",
    "description": "Compare effective state income tax rates for a given income across specified states. Hardcoded rates for the top 10 US states by population.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "income": {
                "type": "number",
                "description": "Annual income in USD to compute state tax on.",
            },
            "states": {
                "type": "array",
                "items": {"type": "string"},
                "description": "List of state abbreviations to compare (e.g. ['CA', 'TX', 'NY']). Supported: CA, NY, TX, FL, WA, IL, PA, OH, NJ, MA.",
            },
        },
        "required": ["income", "states"],
    },
}

# Simplified 2024 state income tax structures
# (brackets as list of (up_to, rate) tuples, or flat rate, or None for no income tax)
_STATE_TAX: dict[str, Any] = {
    "CA": {
        "name": "California",
        "brackets": [
            (10412, 0.01), (24684, 0.02), (38959, 0.04), (54081, 0.06),
            (68350, 0.08), (349137, 0.093), (418961, 0.103),
            (698271, 0.113), (float("inf"), 0.123),
        ],
        "mental_health_surcharge": (1000000, 0.01),  # 1% on income over $1M
    },
    "NY": {
        "name": "New York",
        "brackets": [
            (8500, 0.04), (11700, 0.045), (13900, 0.0525), (80650, 0.0585),
            (215400, 0.0625), (1077550, 0.0685), (5000000, 0.0965),
            (25000000, 0.103), (float("inf"), 0.109),
        ],
    },
    "TX": {"name": "Texas", "brackets": None},
    "FL": {"name": "Florida", "brackets": None},
    "WA": {"name": "Washington", "brackets": None, "note": "7% on long-term capital gains over $250k"},
    "IL": {"name": "Illinois", "flat_rate": 0.0495},
    "PA": {"name": "Pennsylvania", "flat_rate": 0.0307},
    "OH": {
        "name": "Ohio",
        "brackets": [
            (26050, 0.00), (100000, 0.02765), (float("inf"), 0.03688),
        ],
    },
    "NJ": {
        "name": "New Jersey",
        "brackets": [
            (20000, 0.014), (35000, 0.0175), (40000, 0.035),
            (75000, 0.05525), (500000, 0.0637), (1000000, 0.0897),
            (float("inf"), 0.1075),
        ],
    },
    "MA": {"name": "Massachusetts", "flat_rate": 0.05, "millionaire_surcharge": (1000000, 0.04)},
}


def _calc_bracketed_tax(income: float, brackets: list[tuple[float, float]]) -> float:
    """Calculate tax through progressive brackets."""
    tax = 0.0
    prev = 0.0
    for limit, rate in brackets:
        taxable = min(income, limit) - prev
        if taxable <= 0:
            break
        tax += taxable * rate
        prev = limit
    return tax


def _calc_state_tax(income: float, state: str) -> dict[str, Any]:
    """Calculate tax for a single state."""
    cfg = _STATE_TAX[state]
    result: dict[str, Any] = {"state": state, "name": cfg["name"]}

    if cfg.get("brackets") is None and "flat_rate" not in cfg:
        # No income tax state
        result["tax"] = 0.0
        result["effective_rate_pct"] = 0.0
        result["type"] = "no_income_tax"
        if "note" in cfg:
            result["note"] = cfg["note"]
        return result

    if "flat_rate" in cfg:
        tax = income * cfg["flat_rate"]
        # Check for surcharges
        if "millionaire_surcharge" in cfg:
            threshold, surcharge_rate = cfg["millionaire_surcharge"]
            if income > threshold:
                tax += (income - threshold) * surcharge_rate
        result["tax"] = round(tax, 2)
        result["effective_rate_pct"] = round(tax / income * 100, 2) if income > 0 else 0.0
        result["type"] = "flat"
        return result

    tax = _calc_bracketed_tax(income, cfg["brackets"])

    # CA mental health surcharge
    if "mental_health_surcharge" in cfg:
        threshold, rate = cfg["mental_health_surcharge"]
        if income > threshold:
            tax += (income - threshold) * rate

    result["tax"] = round(tax, 2)
    result["effective_rate_pct"] = round(tax / income * 100, 2) if income > 0 else 0.0
    result["type"] = "progressive"
    return result


def state_tax_comparator(
    income: float,
    states: list[str],
) -> dict[str, Any]:
    """Compare effective state income tax rates across states."""
    try:
        if income < 0:
            return {
                "status": "error",
                "data": {"error": "Income must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        normalized = [s.upper().strip() for s in states]
        unsupported = [s for s in normalized if s not in _STATE_TAX]
        if unsupported:
            return {
                "status": "error",
                "data": {"error": f"Unsupported states: {unsupported}. Supported: {list(_STATE_TAX.keys())}"},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        results = [_calc_state_tax(income, s) for s in normalized]
        results_sorted = sorted(results, key=lambda x: x["tax"])

        return {
            "status": "ok",
            "data": {
                "income": round(income, 2),
                "comparison": results_sorted,
                "lowest_tax_state": results_sorted[0]["state"],
                "highest_tax_state": results_sorted[-1]["state"],
                "max_savings": round(results_sorted[-1]["tax"] - results_sorted[0]["tax"], 2),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
