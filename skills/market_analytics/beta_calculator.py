"""
Execuve Summary: Calculates beta, alpha, and related statistics for CAPM analysis.
Inputs: asset_returns (list[float]), market_returns (list[float])
Outputs: beta (float), alpha (float), r_squared (float), residual_risk (float), systematic_pct (float), correlation (float)
MCP Tool Name: beta_calculator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "beta_calculator",
    "description": "Computes beta, correlation, alpha, systematic contribution, and residual risk relative to a benchmark.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "asset_returns": {"type": "array", "description": "Asset return series."},
            "market_returns": {"type": "array", "description": "Benchmark return series."}
        },
        "required": ["asset_returns", "market_returns"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def beta_calculator(**kwargs: Any) -> dict:
    """Calculates beta/correlation and partitions risk into systematic/residual."""
    try:
        asset_returns = kwargs.get("asset_returns")
        market_returns = kwargs.get("market_returns")
        if not isinstance(asset_returns, list) or not isinstance(market_returns, list):
            raise ValueError("asset_returns and market_returns must be lists")
        if len(asset_returns) != len(market_returns) or len(asset_returns) < 2:
            raise ValueError("series must align and contain at least two points")

        asset = [float(r) for r in asset_returns]
        market = [float(r) for r in market_returns]
        mean_asset = sum(asset) / len(asset)
        mean_market = sum(market) / len(market)
        cov = sum((a - mean_asset) * (m - mean_market) for a, m in zip(asset, market)) / (len(asset) - 1)
        var_market = sum((m - mean_market) ** 2 for m in market) / (len(market) - 1)
        var_asset = sum((a - mean_asset) ** 2 for a in asset) / (len(asset) - 1)
        if var_market == 0:
            raise ZeroDivisionError("market variance is zero")
        beta = cov / var_market
        correlation = cov / math.sqrt(var_market * var_asset) if var_asset != 0 else math.nan
        alpha = mean_asset - beta * mean_market
        residual_var = var_asset - beta ** 2 * var_market
        residual_risk = math.sqrt(residual_var) if residual_var > 0 else 0.0
        systematic_pct = (beta ** 2 * var_market) / var_asset if var_asset else math.inf
        r_squared = correlation ** 2 if not math.isnan(correlation) else math.nan

        return {
            "status": "success",
            "data": {
                "beta": beta,
                "alpha": alpha,
                "r_squared": r_squared,
                "residual_risk": residual_risk,
                "systematic_pct": systematic_pct,
                "correlation": correlation
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"beta_calculator failed: {e}")
        _log_lesson(f"beta_calculator: {e}")
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
