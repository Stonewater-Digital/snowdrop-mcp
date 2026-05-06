---
skill: portfolio_stress_test
category: technical
description: Applies historical crash scenarios (2008 GFC, 2020 COVID, Rate Shock) or custom shock tables to a portfolio. Calculates dollar and percentage loss per scenario, identifies the worst-hit asset in each scenario, selects the maximum drawdown scenario overall, and estimates the capital injection needed to recover to the original portfolio value.
tier: free
inputs: portfolio
---

# Portfolio Stress Test

## Description
Applies historical crash scenarios (2008 GFC, 2020 COVID, Rate Shock) or custom shock tables to a portfolio. Calculates dollar and percentage loss per scenario, identifies the worst-hit asset in each scenario, selects the maximum drawdown scenario overall, and estimates the capital injection needed to recover to the original portfolio value.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio` | `array` | Yes |  |
| `scenarios` | `array` | No | Optional custom scenarios. If omitted, defaults are used. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "portfolio_stress_test",
  "arguments": {
    "portfolio": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "portfolio_stress_test"`.
