---
skill: solar_panel_roi_calculator
category: energy_finance
description: Calculate solar panel ROI including federal ITC, annual degradation, payback period, and 25-year total return.
tier: free
inputs: system_cost, annual_production_kwh
---

# Solar Panel Roi Calculator

## Description
Calculate solar panel ROI including federal ITC, annual degradation, payback period, and 25-year total return.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `system_cost` | `number` | Yes | Total system installation cost in USD. |
| `annual_production_kwh` | `number` | Yes | Expected first-year energy production in kWh. |
| `electricity_rate` | `number` | No | Current electricity rate in $/kWh. |
| `annual_degradation` | `number` | No | Annual panel output degradation rate as a decimal. |
| `federal_itc` | `number` | No | Federal Investment Tax Credit rate as a decimal (30% through 2032). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "solar_panel_roi_calculator",
  "arguments": {
    "system_cost": 0,
    "annual_production_kwh": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "solar_panel_roi_calculator"`.
