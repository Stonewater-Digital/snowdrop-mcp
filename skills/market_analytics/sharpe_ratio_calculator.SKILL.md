---
skill: sharpe_ratio_calculator
category: market_analytics
description: Computes annualized Sharpe ratio, return, and volatility for a return series.
tier: free
inputs: returns, risk_free_rate
---

# Sharpe Ratio Calculator

## Description
Computes annualized Sharpe ratio, return, and volatility for a return series.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Periodic strategy returns (decimal). |
| `risk_free_rate` | `number` | Yes | Annual risk-free rate in decimal form. |

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
    "returns": [],
    "risk_free_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sharpe_ratio_calculator"`.
