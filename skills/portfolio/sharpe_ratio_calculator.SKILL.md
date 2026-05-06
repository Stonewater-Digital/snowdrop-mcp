---
skill: sharpe_ratio_calculator
category: portfolio
description: Calculates the Sharpe ratio, measuring risk-adjusted return by comparing excess return over the risk-free rate to portfolio volatility.
tier: free
inputs: returns
---

# Sharpe Ratio Calculator

## Description
Calculates the Sharpe ratio, measuring risk-adjusted return by comparing excess return over the risk-free rate to portfolio volatility.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns (e.g. daily or monthly as decimals). |
| `risk_free_rate` | `number` | No | Risk-free rate per period (default 0.02 annualized). |

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
