---
skill: risk_adjusted_return_calculator
category: personal_finance
description: Calculates risk-adjusted metrics (Sharpe, Sortino, Treynor) plus annualized return/volatility and maximum drawdown from a series of periodic returns.
tier: free
inputs: returns, risk_free_rate
---

# Risk Adjusted Return Calculator

## Description
Calculates risk-adjusted metrics (Sharpe, Sortino, Treynor) plus annualized return/volatility and maximum drawdown from a series of periodic returns.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | List of periodic returns expressed as decimals (e.g., 0.01). |
| `risk_free_rate` | `number` | Yes | Periodic risk-free rate matching the return frequency. |
| `benchmark_returns` | `array` | No | Optional benchmark return series for Treynor ratio. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "risk_adjusted_return_calculator",
  "arguments": {
    "returns": [],
    "risk_free_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_adjusted_return_calculator"`.
