"""
Execuve Summary: Compares sector ETFs on return, volatility, Sharpe, and drawdown.
Inputs: sector_returns (dict[str, list[float]]), period_label (str)
Outputs: total_return_ranked (list[tuple[str, float]]), annualized_vol (dict), sharpe_ranked (list[tuple[str, float]]), max_drawdown (dict), best_sector (str), worst_sector (str)
MCP Tool Name: sector_etf_comparator
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TRADING_DAYS = 252

TOOL_META = {
    "name": "sector_etf_comparator",
    "description": "Ranks sector ETFs by performance metrics over a labelled period.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sector_returns": {"type": "object", "description": "Mapping of ETF ticker to return series."},
            "period_label": {"type": "string", "description": "Label for reporting period."}
        },
        "required": ["sector_returns", "period_label"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def sector_etf_comparator(**kwargs: Any) -> dict:
    """Computes return/vol/met risk metrics for sector ETFs."""
    try:
        sector_returns = kwargs.get("sector_returns")
        period_label = kwargs.get("period_label")
        if not isinstance(sector_returns, dict) or not sector_returns:
            raise ValueError("sector_returns must be non-empty dict")
        if not isinstance(period_label, str):
            raise ValueError("period_label must be string")

        total_returns = {}
        annualized_vol = {}
        sharpe_scores = {}
        max_drawdown = {}
        for name, returns in sector_returns.items():
            if not isinstance(returns, list) or len(returns) == 0:
                continue
            total_returns[name] = sum(returns)
            mean_return = sum(returns) / len(returns)
            variance = sum((r - mean_return) ** 2 for r in returns) / (len(returns) - 1)
            vol = math.sqrt(variance) * math.sqrt(TRADING_DAYS)
            annualized_vol[name] = vol
            sharpe_scores[name] = (mean_return * TRADING_DAYS) / vol if vol else math.inf
            equity = 1.0
            peak = 1.0
            worst = 0.0
            for r in returns:
                equity *= (1 + r)
                peak = max(peak, equity)
                drawdown = equity / peak - 1
                worst = min(worst, drawdown)
            max_drawdown[name] = worst

        ranked_returns = sorted(total_returns.items(), key=lambda item: item[1], reverse=True)
        ranked_sharpe = sorted(sharpe_scores.items(), key=lambda item: item[1], reverse=True)
        best_sector = ranked_returns[0][0] if ranked_returns else None
        worst_sector = ranked_returns[-1][0] if ranked_returns else None

        return {
            "status": "success",
            "data": {
                "total_return_ranked": ranked_returns,
                "annualized_vol": annualized_vol,
                "sharpe_ranked": ranked_sharpe,
                "max_drawdown": max_drawdown,
                "best_sector": best_sector,
                "worst_sector": worst_sector,
                "period_label": period_label
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"sector_etf_comparator failed: {e}")
        _log_lesson(f"sector_etf_comparator: {e}")
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
