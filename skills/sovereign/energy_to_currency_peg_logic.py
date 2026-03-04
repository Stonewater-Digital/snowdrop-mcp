"""
Executive Summary: Models IoT/solar-backed currency pegs, computing intrinsic value per unit and stress-testing peg sustainability across energy price scenarios.
Inputs: energy_data (dict: kwh_produced_daily, energy_price_per_kwh, currency_units_issued, backing_ratio)
Outputs: intrinsic_value_per_unit (float), peg_sustainable (bool), stress_test_results (list[dict]), reserve_adequacy (float)
MCP Tool Name: energy_to_currency_peg_logic
"""
import os
import logging
from typing import Any
from datetime import datetime, timezone

logger = logging.getLogger("snowdrop.skills")

TOOL_META = {
    "name": "energy_to_currency_peg_logic",
    "description": "Models energy-backed currency pegs (IoT/solar), computing intrinsic unit value and stress-testing sustainability across energy price scenarios.",
    "inputSchema": {
        "type": "object",
        "properties": {
            "energy_data": {
                "type": "object",
                "description": "Energy production and currency issuance data",
                "properties": {
                    "kwh_produced_daily": {"type": "number", "description": "Daily kWh energy production"},
                    "energy_price_per_kwh": {"type": "number", "description": "Market price per kWh in USD"},
                    "currency_units_issued": {"type": "number", "description": "Total currency units in circulation"},
                    "backing_ratio": {"type": "number", "description": "Required energy backing ratio (1.0 = 100% backed, 1.2 = 120%)"},
                    "annualization_days": {"type": "integer", "description": "Days per year for annualization (default: 365)"},
                    "reserve_buffer_pct": {"type": "number", "description": "Additional reserve buffer % above peg (default: 10)"}
                },
                "required": ["kwh_produced_daily", "energy_price_per_kwh", "currency_units_issued", "backing_ratio"]
            },
            "stress_scenarios": {
                "type": "array",
                "items": {"type": "number"},
                "description": "Energy price multipliers to test (e.g. [0.5, 0.75, 1.0, 1.25, 1.5]). Default applied if omitted."
            }
        },
        "required": ["energy_data"]
    },
    "outputSchema": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "intrinsic_value_per_unit": {"type": "number"},
                    "peg_sustainable": {"type": "boolean"},
                    "stress_test_results": {"type": "array"},
                    "reserve_adequacy": {"type": "number"}
                }
            },
            "timestamp": {"type": "string"}
        },
        "required": ["status", "data", "timestamp"]
    }
}

# Default stress scenarios: energy price multipliers representing market shocks
DEFAULT_STRESS_SCENARIOS = [0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 2.00]


def _compute_intrinsic_value(
    kwh_daily: float,
    energy_price: float,
    units_issued: float,
    annualization_days: int = 365,
) -> float:
    """Compute the intrinsic value per currency unit from daily energy production.

    Model: Annual energy value / units issued
    Annual energy value = kWh/day * days/year * price/kWh

    Args:
        kwh_daily: Daily kWh energy output.
        energy_price: Market price per kWh in USD.
        units_issued: Total currency units in circulation.
        annualization_days: Days per year (default: 365).

    Returns:
        float: USD value per currency unit.
    """
    if units_issued <= 0:
        raise ValueError("units_issued must be positive")
    annual_energy_value = kwh_daily * annualization_days * energy_price
    return annual_energy_value / units_issued


def energy_to_currency_peg_logic(
    energy_data: dict[str, Any],
    stress_scenarios: list[float] | None = None,
    **kwargs: Any
) -> dict[str, Any]:
    """Model an energy-backed currency peg and stress-test its sustainability.

    The peg is considered sustainable when:
      annual_energy_revenue / (units_issued * peg_price) >= backing_ratio

    Intrinsic value per unit = annual_energy_value / units_issued.
    Reserve adequacy = intrinsic_value / (1.0 / backing_ratio) — how many
    times over the required backing is met.

    Stress tests apply energy price multipliers to simulate commodity shocks,
    renewable curtailment, and demand destruction scenarios.

    Args:
        energy_data: Dictionary containing:
            - kwh_produced_daily (float): Daily energy production in kWh.
            - energy_price_per_kwh (float): Current market price per kWh in USD.
            - currency_units_issued (float): Total currency in circulation.
            - backing_ratio (float): Required backing ratio (1.0 = fully backed).
            - annualization_days (int, optional): Days per year (default: 365).
            - reserve_buffer_pct (float, optional): Additional buffer % (default: 10).
        stress_scenarios: List of energy price multipliers to simulate (e.g.
            [0.5, 1.0, 1.5]). Defaults to DEFAULT_STRESS_SCENARIOS.
        **kwargs: Ignored extra keyword arguments.

    Returns:
        dict: Standard Snowdrop response envelope with keys:
            - status (str): 'success' or 'error'.
            - data (dict): Results including intrinsic_value_per_unit (float),
              peg_sustainable (bool), stress_test_results (list of dicts with
              scenario details), reserve_adequacy (float), and energy_economics.
            - timestamp (str): ISO-8601 UTC timestamp.
    """
    try:
        kwh_daily = float(energy_data.get("kwh_produced_daily", 0.0))
        energy_price = float(energy_data.get("energy_price_per_kwh", 0.0))
        units_issued = float(energy_data.get("currency_units_issued", 0.0))
        backing_ratio = float(energy_data.get("backing_ratio", 1.0))
        annualization_days = int(energy_data.get("annualization_days", 365))
        reserve_buffer_pct = float(energy_data.get("reserve_buffer_pct", 10.0))

        if kwh_daily <= 0:
            raise ValueError("kwh_produced_daily must be positive")
        if energy_price <= 0:
            raise ValueError("energy_price_per_kwh must be positive")
        if units_issued <= 0:
            raise ValueError("currency_units_issued must be positive")
        if backing_ratio <= 0:
            raise ValueError("backing_ratio must be positive")

        scenarios = stress_scenarios if stress_scenarios else DEFAULT_STRESS_SCENARIOS

        # Base case calculations
        intrinsic_value_per_unit = _compute_intrinsic_value(
            kwh_daily, energy_price, units_issued, annualization_days
        )
        annual_energy_revenue = kwh_daily * annualization_days * energy_price
        required_backing_per_unit = 1.0 / backing_ratio  # USD per unit at peg = 1.0
        reserve_adequacy = round(intrinsic_value_per_unit * backing_ratio, 6)

        # Peg sustainability check (backing_ratio >= 1.0 means fully backed)
        # adequacy_ratio = annual_revenue / (units_issued * target_peg_price)
        # If adequacy_ratio >= backing_ratio, peg is sustainable
        adequacy_ratio = annual_energy_revenue / units_issued  # intrinsic per unit
        peg_sustainable = adequacy_ratio >= (1.0 / backing_ratio) and backing_ratio >= 1.0

        # Stress test scenarios
        stress_test_results: list[dict[str, Any]] = []
        for multiplier in sorted(scenarios):
            multiplier = float(multiplier)
            scenario_price = energy_price * multiplier
            scenario_intrinsic = _compute_intrinsic_value(
                kwh_daily, scenario_price, units_issued, annualization_days
            )
            scenario_revenue = kwh_daily * annualization_days * scenario_price
            scenario_adequacy = scenario_intrinsic * backing_ratio
            scenario_sustainable = scenario_intrinsic >= (1.0 / backing_ratio) and backing_ratio >= 1.0

            # Peg break price: minimum energy price to maintain peg
            # intrinsic >= 1/backing_ratio => price >= units_issued / (kwh_daily * days * backing_ratio)
            peg_break_price = units_issued / (kwh_daily * annualization_days * backing_ratio)

            scenario_label = (
                "SEVERE_CRASH" if multiplier <= 0.25
                else "CRASH" if multiplier <= 0.50
                else "STRESS" if multiplier <= 0.75
                else "BASE" if abs(multiplier - 1.0) < 0.01
                else "UPSIDE" if multiplier <= 1.25
                else "BULL" if multiplier <= 1.50
                else "SUPER_BULL"
            )

            stress_test_results.append({
                "price_multiplier": multiplier,
                "scenario_label": scenario_label,
                "energy_price_per_kwh": round(scenario_price, 6),
                "annual_energy_revenue_usd": round(scenario_revenue, 2),
                "intrinsic_value_per_unit": round(scenario_intrinsic, 6),
                "reserve_adequacy_ratio": round(scenario_adequacy, 6),
                "peg_sustainable": scenario_sustainable,
                "peg_break_price_usd": round(peg_break_price, 6),
                "surplus_deficit_pct": round(
                    (scenario_intrinsic - (1.0 / backing_ratio)) / (1.0 / backing_ratio) * 100, 4
                ),
            })

        # Minimum sustainable price
        min_sustainable_price = round(
            units_issued / (kwh_daily * annualization_days * backing_ratio), 8
        )

        # Buffer adequacy: how far above min price current price sits
        price_buffer_pct = round(
            (energy_price - min_sustainable_price) / min_sustainable_price * 100, 4
        ) if min_sustainable_price > 0 else 0.0

        # Scenarios where peg breaks
        broken_scenarios = [s for s in stress_test_results if not s["peg_sustainable"]]
        stress_resilience = f"{len(stress_test_results) - len(broken_scenarios)}/{len(stress_test_results)} scenarios sustainable"

        result: dict[str, Any] = {
            "intrinsic_value_per_unit": round(intrinsic_value_per_unit, 6),
            "peg_sustainable": peg_sustainable,
            "stress_test_results": stress_test_results,
            "reserve_adequacy": round(reserve_adequacy, 6),
            "adequacy_ratio": round(adequacy_ratio, 6),
            "min_sustainable_price_usd": min_sustainable_price,
            "price_buffer_pct": price_buffer_pct,
            "stress_resilience": stress_resilience,
            "broken_scenarios_count": len(broken_scenarios),
            "energy_economics": {
                "kwh_produced_daily": kwh_daily,
                "energy_price_per_kwh": energy_price,
                "annual_energy_revenue_usd": round(annual_energy_revenue, 2),
                "currency_units_issued": units_issued,
                "backing_ratio": backing_ratio,
                "annualization_days": annualization_days,
                "reserve_buffer_pct": reserve_buffer_pct,
                "kwh_per_currency_unit": round(kwh_daily * annualization_days / units_issued, 6),
            },
        }

        return {
            "status": "success",
            "data": result,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        logger.error(f"energy_to_currency_peg_logic failed: {e}")
        _log_lesson(f"energy_to_currency_peg_logic: {e}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


def _log_lesson(message: str) -> None:
    """Append a lesson/error entry to the shared lessons log.

    Args:
        message: Human-readable error or lesson description to append.
    """
    try:
        os.makedirs("logs", exist_ok=True)
        with open("logs/lessons.md", "a") as f:
            f.write(f"- [{datetime.now(timezone.utc).isoformat()}] {message}\n")
    except Exception as log_err:
        logger.warning(f"_log_lesson write failed: {log_err}")
