---
skill: sortino_ratio_calculator
category: market_analytics
description: Computes Sortino ratio with downside deviation and contextualizes relative to Sharpe.
tier: free
inputs: returns, risk_free_rate
---

# Sortino Ratio Calculator

## Description
Computes Sortino ratio with downside deviation and contextualizes relative to Sharpe.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Periodic returns (decimal). |
| `risk_free_rate` | `number` | Yes | Annual risk-free rate. |
| `target_return` | `number` | No | Optional target return per period. |

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
    "returns": [],
    "risk_free_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sortino_ratio_calculator"`.
