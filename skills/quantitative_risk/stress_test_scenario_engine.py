"""
Executive Summary: Multi-factor stress testing engine applying Basel micro-prudential shocks across equity, rate, FX, and spread sensitivities.
Inputs: portfolio_positions (list[dict]), scenario_shocks (dict), sensitivity_multipliers (dict)
Outputs: total_stressed_pnl (float), pnl_by_risk (dict), position_breakdown (list[dict]), worst_risk_type (str)
MCP Tool Name: stress_test_scenario_engine
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "stress_test_scenario_engine",
    "description": "Applies supervisory stresses to rate, FX, equity, and spread sensitivities to produce capital planning P&L breakdowns.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "portfolio_positions": {
                "type": "array",
                "description": "Portfolio positions with market value and per-risk sensitivities.",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Identifier"},
                        "market_value": {"type": "number", "description": "Current market value"},
                        "sensitivities": {
                            "type": "object",
                            "description": "Risk sensitivities such as beta or DV01 equivalents.",
                            "additionalProperties": {
                                "type": "number",
                                "description": "Sensitivity to the risk type",
                            },
                        },
                    },
                    "required": ["name", "market_value", "sensitivities"],
                },
            },
            "scenario_shocks": {
                "type": "object",
                "description": "Shock magnitudes per supervisory scenario (e.g., -35% equity).",
                "properties": {
                    "equity_shock_pct": {"type": "number", "description": "Equity index shock in decimal"},
                    "rate_shock_bps": {"type": "number", "description": "Parallel rate shock in basis points"},
                    "fx_shock_pct": {"type": "number", "description": "FX depreciation in decimal"},
                    "spread_shock_bps": {"type": "number", "description": "Credit spread shock in basis points"},
                },
                "required": ["equity_shock_pct", "rate_shock_bps", "fx_shock_pct", "spread_shock_bps"],
            },
            "sensitivity_multipliers": {
                "type": "object",
                "description": "Calibration multipliers for each risk type (default 1).",
                "properties": {
                    "equity": {"type": "number", "description": "Global scaling for equity shocks", "default": 1.0},
                    "rates": {"type": "number", "description": "Scaling for DV01 impacts", "default": 1.0},
                    "fx": {"type": "number", "description": "Scaling for FX shocks", "default": 1.0},
                    "spread": {"type": "number", "description": "Scaling for credit spread shocks", "default": 1.0},
                },
            },
        },
        "required": ["portfolio_positions", "scenario_shocks"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Stress results"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def stress_test_scenario_engine(
    portfolio_positions: List[Dict[str, Any]],
    scenario_shocks: Dict[str, float],
    sensitivity_multipliers: Dict[str, float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        if not portfolio_positions:
            raise ValueError("portfolio_positions required")
        multipliers = {"equity": 1.0, "rates": 1.0, "fx": 1.0, "spread": 1.0}
        if sensitivity_multipliers:
            multipliers.update({k: float(v) for k, v in sensitivity_multipliers.items()})

        pnl_by_risk = {"equity": 0.0, "rates": 0.0, "fx": 0.0, "spread": 0.0}
        breakdown = []
        for position in portfolio_positions:
            sensitivities = position.get("sensitivities", {})
            equity = sensitivities.get("equity", 0.0) * scenario_shocks.get("equity_shock_pct", 0.0)
            rates = sensitivities.get("rates", 0.0) * scenario_shocks.get("rate_shock_bps", 0.0) / 10000
            fx = sensitivities.get("fx", 0.0) * scenario_shocks.get("fx_shock_pct", 0.0)
            spread = sensitivities.get("spread", 0.0) * scenario_shocks.get("spread_shock_bps", 0.0) / 10000

            equity *= multipliers["equity"]
            rates *= multipliers["rates"]
            fx *= multipliers["fx"]
            spread *= multipliers["spread"]

            pnl_by_risk["equity"] += equity
            pnl_by_risk["rates"] += rates
            pnl_by_risk["fx"] += fx
            pnl_by_risk["spread"] += spread
            breakdown.append(
                {
                    "name": position.get("name"),
                    "equity_pnl": round(equity, 6),
                    "rates_pnl": round(rates, 6),
                    "fx_pnl": round(fx, 6),
                    "spread_pnl": round(spread, 6),
                    "total_pnl": round(equity + rates + fx + spread, 6),
                }
            )

        total_pnl = sum(pnl_by_risk.values())
        worst_risk_type = max(pnl_by_risk, key=lambda k: abs(pnl_by_risk[k]))

        data = {
            "total_stressed_pnl": round(total_pnl, 6),
            "pnl_by_risk": {k: round(v, 6) for k, v in pnl_by_risk.items()},
            "position_breakdown": breakdown,
            "worst_risk_type": worst_risk_type,
            "scenario_description": scenario_shocks,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"stress_test_scenario_engine failed: {e}")
        _log_lesson(f"stress_test_scenario_engine: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    try:
        with open("logs/lessons.md", "a", encoding="utf-8") as handle:
            handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except OSError:
        pass
