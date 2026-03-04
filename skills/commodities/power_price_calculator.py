"""Compute spark and dark spreads for power generation."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

TOOL_META: dict[str, Any] = {
    "name": "power_price_calculator",
    "description": (
        "Calculates spark spread (gas-fired margin), dark spread (coal-fired margin), "
        "clean spark/dark spreads (including carbon cost), and generation dispatch signal."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "electricity_price_per_mwh": {
                "type": "number",
                "description": "Power market price per MWh (must be > 0).",
            },
            "gas_price_per_mmbtu": {
                "type": "number",
                "description": "Natural gas price per MMBtu (must be > 0).",
            },
            "gas_heat_rate": {
                "type": "number",
                "description": "Gas plant heat rate in MMBtu/MWh (must be > 0, typically 7–10).",
            },
            "carbon_price_per_tonne": {
                "type": "number",
                "default": 0.0,
                "description": "Carbon allowance price per tonne CO2 (optional, for clean spreads).",
            },
            "gas_emission_factor_tonnes_per_mwh": {
                "type": "number",
                "default": 0.411,
                "description": "Gas plant CO2 emission factor in tonnes/MWh (default 0.411 t/MWh for CCGT).",
            },
            "coal_price_per_mmbtu": {
                "type": ["number", "null"],
                "default": None,
                "description": "Coal price per MMBtu (optional, required for dark spread).",
            },
            "coal_heat_rate": {
                "type": ["number", "null"],
                "default": None,
                "description": "Coal plant heat rate in MMBtu/MWh (optional, typically 9–11).",
            },
            "coal_emission_factor_tonnes_per_mwh": {
                "type": "number",
                "default": 0.820,
                "description": "Coal plant CO2 emission factor in tonnes/MWh (default 0.82 t/MWh).",
            },
        },
        "required": ["electricity_price_per_mwh", "gas_price_per_mmbtu", "gas_heat_rate"],
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string", "enum": ["success", "error"]},
            "spark_spread_per_mwh": {"type": "number"},
            "clean_spark_spread_per_mwh": {"type": "number"},
            "dark_spread_per_mwh": {"type": ["number", "null"]},
            "clean_dark_spread_per_mwh": {"type": ["number", "null"]},
            "generation_signal": {"type": "string"},
            "timestamp": {"type": "string"},
        },
    },
}


def power_price_calculator(
    electricity_price_per_mwh: float,
    gas_price_per_mmbtu: float,
    gas_heat_rate: float,
    carbon_price_per_tonne: float = 0.0,
    gas_emission_factor_tonnes_per_mwh: float = 0.411,
    coal_price_per_mmbtu: float | None = None,
    coal_heat_rate: float | None = None,
    coal_emission_factor_tonnes_per_mwh: float = 0.820,
    **_: Any,
) -> dict[str, Any]:
    """Return spark and dark spreads with optional carbon cost adjustment.

    Args:
        electricity_price_per_mwh: Power price in $/MWh.
        gas_price_per_mmbtu: Gas price in $/MMBtu.
        gas_heat_rate: Gas plant heat rate in MMBtu/MWh.
        carbon_price_per_tonne: Carbon credit price in $/tonne CO2. Default 0.
        gas_emission_factor_tonnes_per_mwh: CO2 intensity of gas plant. Default 0.411.
        coal_price_per_mmbtu: Coal price in $/MMBtu (optional).
        coal_heat_rate: Coal plant heat rate in MMBtu/MWh (optional).
        coal_emission_factor_tonnes_per_mwh: CO2 intensity of coal plant. Default 0.820.

    Returns:
        dict with status, spark_spread, clean_spark_spread, dark_spread (if coal provided),
        clean_dark_spread (if coal provided), and generation_signal.

    Formulas:
        spark_spread = electricity_price - gas_heat_rate * gas_price
        clean_spark  = spark_spread - carbon_price * gas_emission_factor

        dark_spread  = electricity_price - coal_heat_rate * coal_price
        clean_dark   = dark_spread - carbon_price * coal_emission_factor

    Generation signal:
        Dispatch the plant with the highest clean spread (if > 0).
        If all spreads negative, signal is 'no_dispatch'.
    """
    try:
        if electricity_price_per_mwh <= 0:
            raise ValueError("electricity_price_per_mwh must be positive")
        if gas_price_per_mmbtu <= 0:
            raise ValueError("gas_price_per_mmbtu must be positive")
        if gas_heat_rate <= 0:
            raise ValueError("gas_heat_rate must be positive")

        # Spark spread and clean spark spread
        gas_fuel_cost = gas_heat_rate * gas_price_per_mmbtu
        gas_carbon_cost = carbon_price_per_tonne * gas_emission_factor_tonnes_per_mwh
        spark_spread = electricity_price_per_mwh - gas_fuel_cost
        clean_spark_spread = spark_spread - gas_carbon_cost

        # Dark spread (coal) if inputs provided
        dark_spread: float | None = None
        clean_dark_spread: float | None = None
        if coal_price_per_mmbtu is not None and coal_heat_rate is not None:
            if coal_price_per_mmbtu <= 0:
                raise ValueError("coal_price_per_mmbtu must be positive")
            if coal_heat_rate <= 0:
                raise ValueError("coal_heat_rate must be positive")
            coal_fuel_cost = coal_heat_rate * coal_price_per_mmbtu
            coal_carbon_cost = carbon_price_per_tonne * coal_emission_factor_tonnes_per_mwh
            dark_spread = electricity_price_per_mwh - coal_fuel_cost
            clean_dark_spread = dark_spread - coal_carbon_cost

        # Generation signal based on clean spreads
        if clean_dark_spread is not None:
            if clean_spark_spread <= 0 and clean_dark_spread <= 0:
                signal = "no_dispatch"
            elif clean_spark_spread >= clean_dark_spread:
                signal = "run_gas"
            else:
                signal = "run_coal"
        else:
            signal = "run_gas" if clean_spark_spread > 0 else "no_dispatch"

        return {
            "status": "success",
            "spark_spread_per_mwh": round(spark_spread, 2),
            "clean_spark_spread_per_mwh": round(clean_spark_spread, 2),
            "dark_spread_per_mwh": round(dark_spread, 2) if dark_spread is not None else None,
            "clean_dark_spread_per_mwh": round(clean_dark_spread, 2) if clean_dark_spread is not None else None,
            "generation_signal": signal,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as exc:
        _log_lesson("power_price_calculator", str(exc))
        return {
            "status": "error",
            "error": str(exc),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(skill_name: str, error: str) -> None:
    with open("logs/lessons.md", "a", encoding="utf-8") as handle:
        handle.write(f"- [{datetime.now(timezone.utc).isoformat()}] {skill_name}: {error}\n")
