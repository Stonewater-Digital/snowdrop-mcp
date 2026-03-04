"""
Executive Summary: 2008/2020-style crash simulations — applies historical shock scenarios to a portfolio and reports loss, worst-hit assets, and capital needed for recovery.
Inputs: portfolio (list of dicts: asset str, allocation_pct float, current_value float),
        scenarios (list of dicts: name str, shocks dict[asset_class→drawdown_pct], optional — defaults provided)
Outputs: scenario_results (list of dicts), max_drawdown_scenario (str), recovery_capital_needed (float)
MCP Tool Name: portfolio_stress_test
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

# Default stress scenarios — drawdown_pct values are negative (losses)
DEFAULT_SCENARIOS: list[dict[str, Any]] = [
    {
        "name": "2008 GFC",
        "shocks": {
            "equities": -50.0,
            "re":       -30.0,
            "bonds":    +5.0,
            "crypto":   -80.0,
            "cash":     0.0,
        },
    },
    {
        "name": "2020 COVID",
        "shocks": {
            "equities": -35.0,
            "re":       -10.0,
            "bonds":    +10.0,
            "crypto":   -50.0,
            "cash":     0.0,
        },
    },
    {
        "name": "Rate Shock",
        "shocks": {
            "bonds":    -20.0,
            "equities": -15.0,
            "re":       -25.0,
            "crypto":   -40.0,
            "cash":     0.0,
        },
    },
]

# Asset class keywords — maps portfolio asset names to scenario shock categories
ASSET_CLASS_MAP: dict[str, str] = {
    "stock":   "equities", "equity": "equities", "etf": "equities",
    "spy":     "equities", "qqq":   "equities", "vti": "equities",
    "real_estate": "re",   "reit":  "re",        "property": "re",
    "bond":    "bonds",    "tlt":   "bonds",     "treasury": "bonds",
    "bnd":     "bonds",    "fixed":  "bonds",
    "bitcoin": "crypto",   "btc":   "crypto",    "eth":    "crypto",
    "crypto":  "crypto",   "sol":   "crypto",    "ton":    "crypto",
    "cash":    "cash",     "usdc":  "cash",      "usdt":   "cash",
    "stablecoin": "cash",
}

TOOL_META = {
    "name": "portfolio_stress_test",
    "description": (
        "Applies historical crash scenarios (2008 GFC, 2020 COVID, Rate Shock) or "
        "custom shock tables to a portfolio. Calculates dollar and percentage loss per "
        "scenario, identifies the worst-hit asset in each scenario, selects the maximum "
        "drawdown scenario overall, and estimates the capital injection needed to recover "
        "to the original portfolio value."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "asset":          {"type": "string"},
                        "allocation_pct": {"type": "number"},
                        "current_value":  {"type": "number"},
                    },
                    "required": ["asset", "allocation_pct", "current_value"],
                },
            },
            "scenarios": {
                "type": "array",
                "description": "Optional custom scenarios. If omitted, defaults are used.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name":   {"type": "string"},
                        "shocks": {
                            "type": "object",
                            "additionalProperties": {"type": "number"},
                        },
                    },
                    "required": ["name", "shocks"],
                },
            },
        },
        "required": ["portfolio"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "scenario_results":       {"type": "array"},
            "max_drawdown_scenario":  {"type": "string"},
            "recovery_capital_needed": {"type": "number"},
            "portfolio_total_value":  {"type": "number"},
            "status":                 {"type": "string"},
            "timestamp":              {"type": "string"},
        },
        "required": [
            "scenario_results", "max_drawdown_scenario",
            "recovery_capital_needed", "portfolio_total_value", "status", "timestamp"
        ],
    },
}


def _classify_asset(asset_name: str) -> str:
    """Map a portfolio asset name to a stress-scenario asset class.

    Args:
        asset_name: Raw asset name or ticker from the portfolio.

    Returns:
        Asset class string: "equities", "re", "bonds", "crypto", or "cash".
        Defaults to "equities" for unrecognised assets.
    """
    lower: str = asset_name.lower()
    for keyword, asset_class in ASSET_CLASS_MAP.items():
        if keyword in lower:
            return asset_class
    return "equities"  # conservative default


def portfolio_stress_test(
    portfolio: list[dict[str, Any]],
    scenarios: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Apply historical crash scenarios to a portfolio and report stress outcomes.

    Args:
        portfolio: List of position descriptors. Each dict must contain:
            - asset (str): Asset name or ticker (used for class classification).
            - allocation_pct (float): Percentage of total portfolio (0–100).
            - current_value (float): Current USD value of this position.
        scenarios (list[dict] | None): Optional custom shock scenarios. Each dict
            must contain:
            - name (str): Human-readable scenario name.
            - shocks (dict[str, float]): Asset class → drawdown percentage
              (negative = loss, positive = gain). Uses DEFAULT_SCENARIOS if None.

    Returns:
        dict with keys:
            - status (str): "success" or "error".
            - scenario_results (list[dict]): Per-scenario outcome with:
              scenario_name, portfolio_loss_pct, portfolio_loss_usd,
              portfolio_value_after, worst_hit_asset (dict).
            - max_drawdown_scenario (str): Name of the worst-case scenario.
            - recovery_capital_needed (float): USD needed to restore peak value
              after the worst scenario.
            - portfolio_total_value (float): Current total portfolio value.
            - timestamp (str): ISO 8601 UTC execution timestamp.
    """
    try:
        now_utc: datetime = datetime.now(timezone.utc)

        active_scenarios: list[dict[str, Any]] = scenarios if scenarios else DEFAULT_SCENARIOS

        portfolio_total: float = sum(float(p.get("current_value", 0.0)) for p in portfolio)

        if portfolio_total <= 0:
            raise ValueError("Portfolio total value must be positive.")

        scenario_results: list[dict[str, Any]] = []
        max_loss_usd: float = 0.0
        max_drawdown_scenario_name: str = ""

        for scenario in active_scenarios:
            scenario_name: str = str(scenario.get("name", "Unknown"))
            shocks: dict[str, float] = {
                k.lower(): float(v) for k, v in scenario.get("shocks", {}).items()
            }

            total_loss_usd: float = 0.0
            worst_hit_asset: dict[str, Any] = {"asset": "", "loss_usd": 0.0, "drawdown_pct": 0.0}

            for position in portfolio:
                asset: str = str(position.get("asset", ""))
                pos_value: float = float(position.get("current_value", 0.0))
                asset_class: str = _classify_asset(asset)

                # Apply shock — default to 0 if asset class not in scenario
                shock_pct: float = shocks.get(asset_class, 0.0)
                loss_usd: float = pos_value * (shock_pct / 100.0)
                total_loss_usd += loss_usd  # loss_usd is negative for drawdowns

                if loss_usd < worst_hit_asset["loss_usd"]:
                    worst_hit_asset = {
                        "asset":        asset,
                        "asset_class":  asset_class,
                        "loss_usd":     round(loss_usd, 2),
                        "drawdown_pct": shock_pct,
                        "position_value": pos_value,
                    }

            portfolio_loss_pct: float = (total_loss_usd / portfolio_total) * 100.0
            portfolio_value_after: float = portfolio_total + total_loss_usd  # total_loss is negative

            scenario_results.append(
                {
                    "scenario_name":        scenario_name,
                    "portfolio_loss_pct":   round(portfolio_loss_pct, 4),
                    "portfolio_loss_usd":   round(total_loss_usd, 2),
                    "portfolio_value_after": round(portfolio_value_after, 2),
                    "worst_hit_asset":      worst_hit_asset,
                }
            )

            if total_loss_usd < max_loss_usd:
                max_loss_usd = total_loss_usd
                max_drawdown_scenario_name = scenario_name

        # Recovery capital = amount needed to bring portfolio back to current value
        # from its worst-case post-shock value
        worst_result: dict[str, Any] = min(scenario_results, key=lambda r: r["portfolio_loss_usd"])
        recovery_capital_needed: float = round(abs(worst_result["portfolio_loss_usd"]), 2)

        return {
            "status":                  "success",
            "scenario_results":        scenario_results,
            "max_drawdown_scenario":   max_drawdown_scenario_name or worst_result["scenario_name"],
            "recovery_capital_needed": recovery_capital_needed,
            "portfolio_total_value":   round(portfolio_total, 2),
            "timestamp":               now_utc.isoformat(),
        }

    except Exception as e:
        logger.error(f"portfolio_stress_test failed: {e}")
        _log_lesson(f"portfolio_stress_test: {e}")
        return {"status": "error", "error": str(e), "timestamp": datetime.now(timezone.utc).isoformat()}


def _log_lesson(message: str) -> None:
    """Append a failure lesson to the shared lessons log.

    Args:
        message: Human-readable description of the failure.
    """
    with open("logs/lessons.md", "a") as f:
        f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
