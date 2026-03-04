"""Aggregate commodity exposures and risk diagnostics."""
from __future__ import annotations

import math
from datetime import datetime, timezone
from typing import Any, Iterable

TOOL_META: dict[str, Any] = {
    "name": "commodity_risk_dashboard",
    "description": (
        "Aggregates gross/net notional, parametric 1-day 95% VaR per position, "
        "portfolio VaR proxy, oil-beta weighted exposure, and concentration flags."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "positions": {
                "type": "array",
                "description": "List of commodity positions.",
                "items": {
                    "type": "object",
                    "properties": {
                        "commodity": {
                            "type": "string",
                            "description": "Commodity name or ticker.",
                        },
                        "notional_usd": {
                            "type": "number",
                            "description": "Position notional in USD (positive = long, negative = short).",
                        },
                        "volatility_pct_annual": {
                            "type": "number",
                            "description": "Annualized price volatility in % (must be > 0).",
                        },
                        "correlation_to_oil": {
                            "type": "number",
                            "default": 0.5,
                            "description": "Correlation of this commodity to crude oil (−1 to 1).",
                        },
                    },
                    "required": ["commodity", "notional_usd", "volatility_pct_annual"],
                },
                "minItems": 1,
            },
            "confidence_level": {
                "type": "number",
                "default": 1.645,
                "description": "Z-score for VaR confidence level (1.645 = 95%, 2.326 = 99%). Defaults to 1.645.",
            },
        },
        "required": ["positions"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "gross_notional_usd": {"type": "number"},
            "net_notional_usd": {"type": "number"},
            "position_var": {"type": "array"},
            "largest_var_contributor": {"type": "object"},
            "portfolio_var_usd": {"type": "number"},
            "oil_beta_proxy": {"type": "number"},
            "concentration_flag": {"type": "boolean"},
            "timestamp": {"type": "string"},
        },
    },
}


def commodity_risk_dashboard(
    positions: Iterable[dict[str, Any]],
    confidence_level: float = 1.645,
    **_: Any,
) -> dict[str, Any]:
    """Return aggregated exposure stats and parametric VaR.

    Args:
        positions: Iterable of position dicts with commodity, notional_usd,
            volatility_pct_annual, and optional correlation_to_oil.
        confidence_level: Z-score for VaR (1.645 = 95%, 2.326 = 99%). Default 1.645.

    Returns:
        dict with status, gross/net notional, per-position 1-day VaR, portfolio VaR proxy,
        oil-beta proxy, and concentration flag.

    1-day parametric VaR per position:
        daily_vol = annual_vol_pct / sqrt(252)
        VaR_1d = |notional_usd| * (daily_vol / 100) * z_score

    Portfolio VaR (independent, conservative sum of VaRs as upper bound; actual
    portfolio VaR requires correlation matrix):
        portfolio_VaR <= sum(individual VaRs)

    Concentration flag: largest single VaR > 40% of gross notional.
    Oil-beta proxy: VaR-weighted average correlation_to_oil across positions.
    """
    try:
        position_list = list(positions)
        if not position_list:
            raise ValueError("positions cannot be empty")
        if confidence_level <= 0:
            raise ValueError("confidence_level must be positive")

        gross = sum(abs(float(pos["notional_usd"])) for pos in position_list)
        net = sum(float(pos["notional_usd"]) for pos in position_list)

        position_var = []
        for pos in position_list:
            notional = float(pos["notional_usd"])
            annual_vol = float(pos["volatility_pct_annual"])
            if annual_vol <= 0:
                raise ValueError(f"volatility_pct_annual must be > 0 for '{pos.get('commodity')}'")
            daily_vol_frac = (annual_vol / 100.0) / math.sqrt(252.0)
            var_1d = abs(notional) * daily_vol_frac * confidence_level
            corr_oil = float(pos.get("correlation_to_oil", 0.5))
            position_var.append(
                {
                    "commodity": pos["commodity"],
                    "notional_usd": round(notional, 2),
                    "var_1d_usd": round(var_1d, 2),
                    "annual_vol_pct": round(annual_vol, 2),
                    "correlation_to_oil": corr_oil,
                }
            )

        # Largest VaR contributor
        top = max(position_var, key=lambda item: item["var_1d_usd"])

        # Portfolio VaR: conservative sum (no netting correlations provided)
        portfolio_var = sum(item["var_1d_usd"] for item in position_var)

        # Oil-beta proxy: VaR-weighted avg correlation to oil
        total_var = sum(item["var_1d_usd"] for item in position_var) or 1e-12
        oil_beta = (
            sum(item["var_1d_usd"] * item["correlation_to_oil"] for item in position_var) / total_var
        )

        # Concentration: single largest VaR > 40% of sum of VaRs
        concentration_flag = top["var_1d_usd"] / total_var > 0.40

        return {
            "status": "success",
            "gross_notional_usd": round(gross, 2),
            "net_notional_usd": round(net, 2),
            "position_var": position_var,
            "largest_var_contributor": top,
            "portfolio_var_usd": round(portfolio_var, 2),
            "oil_beta_proxy": round(oil_beta, 3),
            "concentration_flag": concentration_flag,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("commodity_risk_dashboard", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
