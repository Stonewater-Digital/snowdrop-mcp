---
skill: calmar_ratio_calculator
category: market_analytics
description: Computes the Calmar ratio using cumulative returns and drawdown analysis.
tier: free
inputs: returns, period_years
---

# Calmar Ratio Calculator

## Description
Computes the Calmar ratio using cumulative returns and drawdown analysis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Periodic returns (decimal). |
| `period_years` | `number` | Yes | Total time span of the series in years. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "calmar_ratio_calculator",
  "arguments": {
    "returns": [],
    "period_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "calmar_ratio_calculator"`.
