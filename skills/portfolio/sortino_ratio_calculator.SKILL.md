---
skill: sortino_ratio_calculator
category: portfolio
description: Calculates the Sortino ratio, a variation of the Sharpe ratio that only penalizes downside volatility rather than total volatility.
tier: free
inputs: returns
---

# Sortino Ratio Calculator

## Description
Calculates the Sortino ratio, a variation of the Sharpe ratio that only penalizes downside volatility rather than total volatility.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns as decimals. |
| `risk_free_rate` | `number` | No | Risk-free rate per period (default 0.02). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "sortino_ratio_calculator",
  "arguments": {
    "returns": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sortino_ratio_calculator"`.
