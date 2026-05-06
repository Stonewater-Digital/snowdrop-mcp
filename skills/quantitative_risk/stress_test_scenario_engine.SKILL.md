---
skill: stress_test_scenario_engine
category: quantitative_risk
description: Applies supervisory stresses to rate, FX, equity, and spread sensitivities to produce capital planning P&L breakdowns.
tier: free
inputs: portfolio_positions, scenario_shocks
---

# Stress Test Scenario Engine

## Description
Applies supervisory stresses to rate, FX, equity, and spread sensitivities to produce capital planning P&L breakdowns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_positions` | `array` | Yes | Portfolio positions with market value and per-risk sensitivities. |
| `scenario_shocks` | `object` | Yes | Shock magnitudes per supervisory scenario (e.g., -35% equity). |
| `sensitivity_multipliers` | `object` | No | Calibration multipliers for each risk type (default 1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "stress_test_scenario_engine",
  "arguments": {
    "portfolio_positions": [],
    "scenario_shocks": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stress_test_scenario_engine"`.
