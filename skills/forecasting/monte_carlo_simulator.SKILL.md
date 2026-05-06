---
skill: monte_carlo_simulator
category: forecasting
description: Runs geometric Brownian motion simulations to generate percentile outcomes.
tier: free
inputs: initial_value, expected_annual_return, annual_volatility, years
---

# Monte Carlo Simulator

## Description
Runs geometric Brownian motion simulations to generate percentile outcomes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `initial_value` | `number` | Yes |  |
| `expected_annual_return` | `number` | Yes |  |
| `annual_volatility` | `number` | Yes |  |
| `years` | `integer` | Yes |  |
| `num_simulations` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "monte_carlo_simulator",
  "arguments": {
    "initial_value": 0,
    "expected_annual_return": 0,
    "annual_volatility": 0,
    "years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "monte_carlo_simulator"`.
