"""Model a private equity J-curve."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "j_curve_modeler",
    "description": "Simulates fund cash flows, NAV, and J-curve inflection metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "fund_size": {"type": "number"},
            "investment_period_years": {"type": "integer", "default": 5},
            "fund_life_years": {"type": "integer", "default": 10},
            "management_fee_pct": {"type": "number", "default": 2.0},
            "deployment_pace": {"type": "array", "items": {"type": "number"}},
            "exit_multiples": {"type": "array", "items": {"type": "object"}},
            "loss_rate_pct": {"type": "number", "default": 15.0},
        },
        "required": ["fund_size", "deployment_pace", "exit_multiples"],
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


def j_curve_modeler(
    fund_size: float,
    investment_period_years: int,
    fund_life_years: int,
    management_fee_pct: float,
    deployment_pace: list[float],
    exit_multiples: list[dict[str, Any]],
    loss_rate_pct: float = 15.0,
    **_: Any,
) -> dict[str, Any]:
    """Return yearly cash flows and NAV for a stylized PE J-curve."""
    try:
        years = list(range(1, fund_life_years + 1))
        pace = deployment_pace + [0.0] * max(0, len(years) - len(deployment_pace))
        loss_rate = loss_rate_pct / 100
        exit_map = {int(item.get("year", 0)): float(item.get("multiple", 1.0)) for item in exit_multiples}
        nav = 0.0
        yearly_cashflows = []
        nav_curve = []
        capital_called_total = 0.0
        total_distributions = 0.0
        for idx, year in enumerate(years, start=1):
            call_pct = pace[idx - 1] if idx - 1 < len(pace) else 0.0
            capital_call = fund_size * (call_pct / 100)
            capital_called_total += capital_call
            fees = fund_size * (management_fee_pct / 100)
            exits = nav * exit_map.get(year, 0.0)
            write_off = nav * loss_rate
            distribution = max(exits - write_off, 0.0)
            total_distributions += distribution
            nav = nav + capital_call - distribution - fees
            nav_curve.append(round(nav, 2))
            yearly_cashflows.append(
                {
                    "year": year,
                    "capital_called": round(capital_call, 2),
                    "fees": round(fees, 2),
                    "distributions": round(distribution, 2),
                    "ending_nav": round(nav, 2),
                }
            )
        trough_nav = min(nav_curve) if nav_curve else 0.0
        trough_year = nav_curve.index(trough_nav) + 1 if nav_curve else 0
        breakeven_year = next((i for i, value in enumerate(nav_curve, start=1) if value >= 0), fund_life_years)
        terminal_tvpi = (total_distributions + nav) / capital_called_total if capital_called_total else 0.0
        terminal_irr = ((total_distributions + nav) / capital_called_total) ** (1 / fund_life_years) - 1 if capital_called_total else 0.0
        data = {
            "yearly_cashflows": yearly_cashflows,
            "j_curve_trough_year": trough_year,
            "trough_tvpi": round(trough_nav / capital_called_total if capital_called_total else 0.0, 2),
            "breakeven_year": breakeven_year,
            "terminal_tvpi": round(terminal_tvpi, 2),
            "terminal_irr": round(terminal_irr, 4),
            "nav_curve": nav_curve,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:  # noqa: BLE001
        _log_lesson("j_curve_modeler", str(exc))
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
