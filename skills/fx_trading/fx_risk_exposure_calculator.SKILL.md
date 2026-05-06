---
skill: fx_risk_exposure_calculator
category: fx_trading
description: Aggregates gross/net FX exposures and estimates VaR.
tier: free
inputs: positions, fx_rates, vol_estimates
---

# Fx Risk Exposure Calculator

## Description
Aggregates gross/net FX exposures and estimates VaR.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `base_currency` | `string` | No |  |
| `fx_rates` | `object` | Yes |  |
| `vol_estimates` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fx_risk_exposure_calculator",
  "arguments": {
    "positions": [],
    "fx_rates": {},
    "vol_estimates": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fx_risk_exposure_calculator"`.
