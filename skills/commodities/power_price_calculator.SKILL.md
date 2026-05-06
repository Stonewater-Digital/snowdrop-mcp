---
skill: power_price_calculator
category: commodities
description: Calculates spark spread (gas-fired margin), dark spread (coal-fired margin), clean spark/dark spreads (including carbon cost), and generation dispatch signal.
tier: free
inputs: electricity_price_per_mwh, gas_price_per_mmbtu, gas_heat_rate
---

# Power Price Calculator

## Description
Calculates spark spread (gas-fired margin), dark spread (coal-fired margin), clean spark/dark spreads (including carbon cost), and generation dispatch signal.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `electricity_price_per_mwh` | `number` | Yes | Power market price per MWh (must be > 0). |
| `gas_price_per_mmbtu` | `number` | Yes | Natural gas price per MMBtu (must be > 0). |
| `gas_heat_rate` | `number` | Yes | Gas plant heat rate in MMBtu/MWh (must be > 0, typically 7–10). |
| `carbon_price_per_tonne` | `number` | No | Carbon allowance price per tonne CO2 (optional, for clean spreads). |
| `gas_emission_factor_tonnes_per_mwh` | `number` | No | Gas plant CO2 emission factor in tonnes/MWh (default 0.411 t/MWh for CCGT). |
| `coal_price_per_mmbtu` | `['number', 'null']` | No | Coal price per MMBtu (optional, required for dark spread). |
| `coal_heat_rate` | `['number', 'null']` | No | Coal plant heat rate in MMBtu/MWh (optional, typically 9–11). |
| `coal_emission_factor_tonnes_per_mwh` | `number` | No | Coal plant CO2 emission factor in tonnes/MWh (default 0.82 t/MWh). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "power_price_calculator",
  "arguments": {
    "electricity_price_per_mwh": 0,
    "gas_price_per_mmbtu": 0,
    "gas_heat_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "power_price_calculator"`.
