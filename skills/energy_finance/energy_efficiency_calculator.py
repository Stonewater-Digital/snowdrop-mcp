"""Calculate energy efficiency and compare to benchmarks.

MCP Tool Name: energy_efficiency_calculator
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "energy_efficiency_calculator",
    "description": "Calculate energy efficiency (useful output / energy input) as a percentage and compare to common benchmarks for various energy systems.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "energy_input": {
                "type": "number",
                "description": "Total energy input (in any consistent unit).",
            },
            "useful_output": {
                "type": "number",
                "description": "Useful energy output (same unit as input).",
            },
        },
        "required": ["energy_input", "useful_output"],
    },
}

_BENCHMARKS = {
    "LED lighting": 90,
    "Electric motor": 85,
    "Heat pump (COP 3)": 300,
    "Natural gas furnace": 95,
    "Solar PV panel": 22,
    "Wind turbine": 45,
    "Coal power plant": 33,
    "Combined cycle gas turbine": 60,
    "Internal combustion engine": 25,
    "Electric vehicle drivetrain": 85,
    "Hydrogen fuel cell": 60,
}


def energy_efficiency_calculator(
    energy_input: float,
    useful_output: float,
) -> dict[str, Any]:
    """Calculate energy efficiency."""
    try:
        if energy_input <= 0:
            return {
                "status": "error",
                "data": {"error": "energy_input must be positive."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        if useful_output < 0:
            return {
                "status": "error",
                "data": {"error": "useful_output must be non-negative."},
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        efficiency = useful_output / energy_input * 100
        waste = energy_input - useful_output
        waste_pct = 100 - efficiency

        return {
            "status": "ok",
            "data": {
                "energy_input": round(energy_input, 4),
                "useful_output": round(useful_output, 4),
                "efficiency_pct": round(efficiency, 2),
                "energy_wasted": round(waste, 4),
                "waste_pct": round(waste_pct, 2),
                "benchmarks": {k: f"{v}%" for k, v in _BENCHMARKS.items()},
                "note": "Heat pumps can exceed 100% efficiency (COP > 1) because they move heat rather than generate it.",
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        return {
            "status": "error",
            "data": {"error": str(exc)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
