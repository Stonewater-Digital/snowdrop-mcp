"""
Executive Summary: Basel IRB capital calculator using corporate correlation formula and maturity adjustment.
Inputs: pd_list (list[float]), lgd_list (list[float]), ead_list (list[float]), maturities (list[float])
Outputs: rwa (float), capital_requirement (float), unexpected_loss (float)
MCP Tool Name: credit_risk_irb_capital
"""
import logging
from datetime import datetime, timezone
from math import exp, log
from statistics import NormalDist
from typing import Any, List

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "credit_risk_irb_capital",
    "description": "Applies Basel IRB corporate formula for rho, maturity adjustment, and capital (K).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "pd_list": {
                "type": "array",
                "description": "Probability of default per obligor (decimals).",
                "items": {"type": "number"},
            },
            "lgd_list": {
                "type": "array",
                "description": "Loss-given-default percentages per obligor.",
                "items": {"type": "number"},
            },
            "ead_list": {
                "type": "array",
                "description": "Exposure at default per obligor.",
                "items": {"type": "number"},
            },
            "maturities": {
                "type": "array",
                "description": "Effective maturity in years (M).",
                "items": {"type": "number"},
            },
        },
        "required": ["pd_list", "lgd_list", "ead_list", "maturities"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "IRB outputs"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def credit_risk_irb_capital(
    pd_list: List[float],
    lgd_list: List[float],
    ead_list: List[float],
    maturities: List[float],
    **_: Any,
) -> dict[str, Any]:
    try:
        n = len(pd_list)
        if not (len(lgd_list) == len(ead_list) == len(maturities) == n):
            raise ValueError("input vectors must match length")
        inv = NormalDist().inv_cdf
        dist = NormalDist()
        total_rwa = 0.0
        expected_loss = 0.0
        unexpected_loss = 0.0
        breakdown = []
        for i in range(n):
            pd = max(min(pd_list[i], 0.999), 1e-6)
            lgd = lgd_list[i] / 100.0
            ead = ead_list[i]
            m = max(maturities[i], 1.0)
            rho = 0.12 * (1 - exp(-50 * pd)) / (1 - exp(-50))
            rho += 0.24 * (1 - (1 - exp(-50 * pd)) / (1 - exp(-50)))
            rho = min(max(rho, 0.03), 0.24)
            k = dist.cdf((1 / ((1 - rho) ** 0.5)) * inv(pd) + ((rho ** 0.5) / ((1 - rho) ** 0.5)) * inv(0.999))
            k = lgd * k - pd * lgd
            maturity_adj = (1 + (m - 2.5) * (0.11852 - 0.05478 * log(pd))) / (1 - 1.5 * log(pd))
            maturity_adj = max(maturity_adj, 0.0)
            capital = k * maturity_adj
            rwa = capital * ead * 12.5
            total_rwa += rwa
            expected_loss_i = pd * lgd * ead
            expected_loss += expected_loss_i
            unexpected_loss += max(capital * ead - expected_loss_i, 0.0)
            breakdown.append(
                {
                    "index": i,
                    "rho": round(rho, 4),
                    "k": round(capital, 6),
                    "rwa": round(rwa, 2),
                    "expected_loss": round(expected_loss_i, 2),
                }
            )
        data = {
            "total_rwa": round(total_rwa, 2),
            "expected_loss": round(expected_loss, 2),
            "unexpected_loss": round(unexpected_loss, 2),
            "capital_requirement": round(total_rwa * 0.08, 2),
            "breakdown": breakdown,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"credit_risk_irb_capital failed: {e}")
        _log_lesson(f"credit_risk_irb_capital: {e}")
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
