"""
Executive Summary: Pillar 3 disclosure metrics aggregator summarizing capital, RWAs, liquidity, and leverage.
Inputs: capital (dict), rwa_by_risk_type (dict), liquidity_metrics (dict), leverage_ratio_pct (float)
Outputs: disclosure_table (list[dict]), key_ratios (dict)
MCP Tool Name: pillar_3_disclosure_generator
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "pillar_3_disclosure_generator",
    "description": "Prepares Pillar 3 style summary of capital ratios, RWAs, LCR/NSFR, and leverage metrics.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "capital": {
                "type": "object",
                "description": "Capital amounts (CET1, Tier1, Total).",
                "properties": {
                    "cet1": {"type": "number", "description": "CET1 capital"},
                    "tier1": {"type": "number", "description": "Tier 1 capital"},
                    "total": {"type": "number", "description": "Total capital"},
                    "rwa": {"type": "number", "description": "Risk-weighted assets"},
                },
                "required": ["cet1", "tier1", "total", "rwa"],
            },
            "rwa_by_risk_type": {
                "type": "object",
                "description": "RWA amounts per risk type.",
                "additionalProperties": {"type": "number", "description": "RWA amount"},
            },
            "liquidity_metrics": {
                "type": "object",
                "description": "Liquidity ratios (LCR, NSFR).",
                "properties": {
                    "lcr_pct": {"type": "number", "description": "Liquidity coverage ratio"},
                    "nsfr_pct": {"type": "number", "description": "Net stable funding ratio"},
                },
                "required": ["lcr_pct", "nsfr_pct"],
            },
            "leverage_ratio_pct": {"type": "number", "description": "Basel leverage ratio."},
        },
        "required": ["capital", "rwa_by_risk_type", "liquidity_metrics", "leverage_ratio_pct"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "Disclosure output"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def pillar_3_disclosure_generator(
    capital: Dict[str, float],
    rwa_by_risk_type: Dict[str, float],
    liquidity_metrics: Dict[str, float],
    leverage_ratio_pct: float,
    **_: Any,
) -> dict[str, Any]:
    try:
        rwa = capital["rwa"]
        ratios = {
            "cet1_ratio_pct": round(capital["cet1"] / rwa * 100 if rwa else 0.0, 2),
            "tier1_ratio_pct": round(capital["tier1"] / rwa * 100 if rwa else 0.0, 2),
            "total_capital_ratio_pct": round(capital["total"] / rwa * 100 if rwa else 0.0, 2),
            "leverage_ratio_pct": round(leverage_ratio_pct, 2),
            "lcr_pct": round(liquidity_metrics["lcr_pct"], 2),
            "nsfr_pct": round(liquidity_metrics["nsfr_pct"], 2),
        }
        disclosure_table = [
            {"metric": "CET1", "amount": round(capital["cet1"], 2), "ratio_pct": ratios["cet1_ratio_pct"]},
            {"metric": "Tier 1", "amount": round(capital["tier1"], 2), "ratio_pct": ratios["tier1_ratio_pct"]},
            {"metric": "Total Capital", "amount": round(capital["total"], 2), "ratio_pct": ratios["total_capital_ratio_pct"]},
        ]
        data = {
            "disclosure_table": disclosure_table,
            "rwa_by_risk_type": {k: round(v, 2) for k, v in rwa_by_risk_type.items()},
            "key_ratios": ratios,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"pillar_3_disclosure_generator failed: {e}")
        _log_lesson(f"pillar_3_disclosure_generator: {e}")
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
