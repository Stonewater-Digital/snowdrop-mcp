"""
Executive Summary: Basel III Liquidity Coverage Ratio applying haircut caps to HQLA and comparing against stressed outflows.
Inputs: hqlas (dict), haircuts (dict), net_cash_outflows (float)
Outputs: lcr_ratio (float), hqlas_after_haircuts (dict), surplus_deficit (float), compliance (str)
MCP Tool Name: liquidity_coverage_ratio
"""
import logging
from datetime import datetime, timezone
from typing import Any, Dict

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "liquidity_coverage_ratio",
    "description": "Basel III LCR computation with supervisory caps on Level 2 assets and haircut adjustments.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "hqlas": {
                "type": "object",
                "description": "High quality liquid asset balances by level (base currency).",
                "properties": {
                    "level1": {"type": "number", "description": "Level 1 HQLA"},
                    "level2a": {"type": "number", "description": "Level 2A HQLA"},
                    "level2b": {"type": "number", "description": "Level 2B HQLA"},
                },
                "required": ["level1", "level2a", "level2b"],
            },
            "haircuts": {
                "type": "object",
                "description": "Haircut percentages per LCR rules (0-100).",
                "properties": {
                    "level1": {"type": "number", "description": "Default 0", "default": 0.0},
                    "level2a": {"type": "number", "description": "Default 15", "default": 15.0},
                    "level2b": {"type": "number", "description": "Default 25", "default": 25.0},
                },
            },
            "net_cash_outflows": {
                "type": "number",
                "description": "30-day stressed net cash outflows as per Basel formula.",
            },
        },
        "required": ["hqlas", "net_cash_outflows"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "description": "status"},
            "data": {"type": "object", "description": "LCR metrics"},
            "timestamp": {"type": "string", "description": "timestamp"},
        },
        "required": ["status", "timestamp"],
    },
}


def liquidity_coverage_ratio(
    hqlas: Dict[str, float],
    net_cash_outflows: float,
    haircuts: Dict[str, float] | None = None,
    **_: Any,
) -> dict[str, Any]:
    try:
        if net_cash_outflows <= 0:
            raise ValueError("net_cash_outflows must be positive")
        levels = {"level1": 0.0, "level2a": 0.0, "level2b": 0.0}
        for level in levels:
            if level not in hqlas:
                raise ValueError(f"missing {level} balance")
            levels[level] = float(hqlas[level])
        hc = {"level1": 0.0, "level2a": 15.0, "level2b": 25.0}
        if haircuts:
            hc.update({k: float(v) for k, v in haircuts.items() if k in hc})
        adjusted = {
            level: amount * (1 - hc[level] / 100.0)
            for level, amount in levels.items()
        }
        level2_total = adjusted["level2a"] + adjusted["level2b"]
        level2_cap = min(level2_total, adjusted["level1"] * 2 / 3)
        level2b_cap = min(adjusted["level2b"], level2_cap, adjusted["level1"] * 0.15)
        level2a_cap = max(level2_cap - level2b_cap, 0.0)
        final_hqla = adjusted["level1"] + min(adjusted["level2a"], level2a_cap) + level2b_cap
        lcr_ratio = final_hqla / net_cash_outflows
        surplus = final_hqla - net_cash_outflows
        compliance = "compliant" if lcr_ratio >= 1.0 else "breach"

        data = {
            "lcr_ratio": round(lcr_ratio * 100, 2),
            "hqlas_after_haircuts": {k: round(v, 2) for k, v in adjusted.items()},
            "final_hqla": round(final_hqla, 2),
            "surplus_deficit": round(surplus, 2),
            "net_cash_outflows": round(net_cash_outflows, 2),
            "compliance": compliance,
        }
        return {
            "status": "success",
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"liquidity_coverage_ratio failed: {e}")
        _log_lesson(f"liquidity_coverage_ratio: {e}")
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
