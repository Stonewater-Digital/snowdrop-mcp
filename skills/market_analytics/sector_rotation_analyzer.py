"""
Execuve Summary: Evaluates sector relative strength versus benchmark.
Inputs: sector_returns (dict[str, list[float]]), benchmark_returns (list[float])
Outputs: relative_strength_per_sector (dict), rotation_phase (dict), momentum_ranking (list[tuple[str, float]])
MCP Tool Name: sector_rotation_analyzer
"""
import logging
import math
from datetime import datetime, timezone
from typing import Any

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "sector_rotation_analyzer",
    "description": "Measures sector relative strength and assigns rotation phases (leading/lagging/etc.).",
    "inputSchema": {
        "type": "object",
        "properties": {
            "sector_returns": {"type": "object", "description": "Mapping of sector name to return list."},
            "benchmark_returns": {"type": "array", "description": "Benchmark return series."}
        },
        "required": ["sector_returns", "benchmark_returns"]
    },
    "outputSchema": {
        "type": "object", "properties": {"status": {"type": "string"}, "timestamp": {"type": "string"}, "data": {"type": "object"}}, "required": ["status", "timestamp"]
    }
}


def sector_rotation_analyzer(**kwargs: Any) -> dict:
    """Computes sector relative strength metrics."""
    try:
        sector_returns = kwargs.get("sector_returns")
        benchmark_returns = kwargs.get("benchmark_returns")
        if not isinstance(sector_returns, dict) or not sector_returns:
            raise ValueError("sector_returns must be non-empty dict")
        if not isinstance(benchmark_returns, list) or len(benchmark_returns) == 0:
            raise ValueError("benchmark_returns must be non-empty list")
        bench_clean = [float(r) for r in benchmark_returns]
        bench_mean = sum(bench_clean) / len(bench_clean)

        relative_strength = {}
        rotation_phase = {}
        ranking = []
        for sector, returns in sector_returns.items():
            if not isinstance(returns, list) or len(returns) != len(bench_clean):
                raise ValueError("each sector return series must align with benchmark length")
            sector_mean = sum(returns) / len(returns)
            momentum = returns[-1]
            rs = sector_mean - bench_mean
            relative_strength[sector] = rs
            ranking.append((sector, sector_mean))
            if rs > 0 and momentum > bench_clean[-1]:
                rotation_phase[sector] = "leading"
            elif rs > 0 and momentum <= bench_clean[-1]:
                rotation_phase[sector] = "weakening"
            elif rs < 0 and momentum > bench_clean[-1]:
                rotation_phase[sector] = "improving"
            else:
                rotation_phase[sector] = "lagging"

        ranking.sort(key=lambda item: item[1], reverse=True)

        return {
            "status": "success",
            "data": {
                "relative_strength_per_sector": relative_strength,
                "rotation_phase": rotation_phase,
                "momentum_ranking": ranking
            },
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except (ValueError, TypeError, ZeroDivisionError) as e:
        logger.error(f"sector_rotation_analyzer failed: {e}")
        _log_lesson(f"sector_rotation_analyzer: {e}")
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
