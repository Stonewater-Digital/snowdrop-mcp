---
skill: sharpe_ratio_calculator
category: middle_office
description: Calculates Sharpe, Sortino, and Calmar ratios from a return series.
tier: free
inputs: returns
---

# Sharpe Ratio Calculator

## Description
Calculates Sharpe, Sortino, and Calmar ratios from a return series.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes |  |
| `risk_free_rate` | `number` | No |  |
| `periods_per_year` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sharpe_ratio_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sharpe_ratio_calculator"`.
