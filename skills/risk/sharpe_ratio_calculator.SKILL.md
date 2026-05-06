---
skill: sharpe_ratio_calculator
category: risk
description: Calculates Sharpe, Sortino, and ancillary performance stats.
tier: free
inputs: returns
---

# Sharpe Ratio Calculator

## Description
Computes risk-adjusted performance metrics for a portfolio or strategy using a series of daily returns. Produces the annualized Sharpe ratio (excess return per unit of total volatility), Sortino ratio (excess return per unit of downside volatility), annualized return, annualized volatility, and the maximum consecutive loss streak. Requires at least two daily return observations. Use to benchmark portfolio performance against the risk-free rate and compare strategies on a risk-adjusted basis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `returns` | `array` | Yes | Ordered list of daily portfolio returns as decimals (e.g. 0.02 = +2%, -0.01 = -1%). Must have at least 2 observations. |
| `risk_free_rate_annual` | `number` | No | Annual risk-free rate as a decimal (e.g. 0.05 = 5%). Defaults to 0.05 (5%). Used to compute excess returns for Sharpe and Sortino. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

Data fields: `sharpe_ratio`, `sortino_ratio`, `annualized_return`, `annualized_volatility`, `max_loss_streak` (integer, longest run of consecutive negative-return days).

## Example
```json
{
  "tool": "sharpe_ratio_calculator",
  "arguments": {
    "returns": [0.012, -0.005, 0.023, -0.018, 0.007, 0.015, -0.003, 0.009, -0.011, 0.021],
    "risk_free_rate_annual": 0.05
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "sharpe_ratio_calculator"`.
