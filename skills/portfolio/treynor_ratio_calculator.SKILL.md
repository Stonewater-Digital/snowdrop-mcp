---
skill: treynor_ratio_calculator
category: portfolio
description: Calculates the Treynor ratio, measuring excess return per unit of systematic risk (beta).
tier: free
inputs: portfolio_return, risk_free_rate, beta
---

# Treynor Ratio Calculator

## Description
Calculates the Treynor ratio, measuring excess return per unit of systematic risk (beta).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `portfolio_return` | `number` | Yes | Portfolio return for the period (decimal). |
| `risk_free_rate` | `number` | Yes | Risk-free rate for the period (decimal). |
| `beta` | `number` | Yes | Portfolio beta relative to the market. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "treynor_ratio_calculator",
  "arguments": {
    "portfolio_return": 0,
    "risk_free_rate": 0,
    "beta": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "treynor_ratio_calculator"`.
