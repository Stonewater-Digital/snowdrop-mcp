---
skill: historical_var_calculator
category: quantitative_risk
description: Historical simulation VaR/ES with Kupiec backtest p-value using equal or exponential age weights.
tier: free
inputs: historical_returns, confidence_level, horizon_days, portfolio_weights
---

# Historical Var Calculator

## Description
Historical simulation VaR/ES with Kupiec backtest p-value using equal or exponential age weights.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `historical_returns` | `array` | Yes | Matrix of historical asset returns, each row is one observation with decimals. |
| `confidence_level` | `number` | Yes | Confidence level such as 0.99 for 99% VaR. |
| `horizon_days` | `integer` | Yes | Forecast horizon in days for square-root-of-time scaling. |
| `portfolio_weights` | `array` | Yes | Portfolio weights corresponding to assets in the historical matrix. |
| `weighting_scheme` | `string` | No | equal for standard Basel HS VaR or age for exponentially weighted (lambda=0.97). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "historical_var_calculator",
  "arguments": {
    "historical_returns": [],
    "confidence_level": 0,
    "horizon_days": 0,
    "portfolio_weights": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "historical_var_calculator"`.
