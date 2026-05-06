---
skill: value_at_risk
category: risk
description: Computes multi-level VaR and CVaR via historical simulation.
tier: free
inputs: positions, holding_period_days
---

# Value At Risk

## Description
Computes portfolio Value at Risk (VaR) and Conditional VaR (Expected Shortfall) using historical simulation. Each position provides an asset label, current dollar value, and a list of historical daily returns. VaR is scaled to the specified holding period using the square-root-of-time rule. Returns loss thresholds at each confidence level alongside the expected shortfall (average loss beyond VaR). Use for portfolio-level risk measurement and capital allocation decisions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes | List of position objects, each with `asset` (string), `value` (number, current USD value), and `daily_returns` (array of floats representing historical daily P&L as decimals). |
| `holding_period_days` | `integer` | Yes | Number of trading days over which to measure risk (e.g. 1 for daily VaR, 10 for 2-week regulatory VaR). Must be positive. |
| `confidence_levels` | `array` | No | Confidence levels to compute VaR at, as decimals (e.g. [0.95, 0.99]). Defaults to [0.95, 0.99]. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

Data fields: `portfolio_value` (total USD), `var` (object keyed by confidence level, e.g. `"95pct"`), `expected_shortfall` (CVaR per confidence level), `holding_period_days`.

## Example
```json
{
  "tool": "value_at_risk",
  "arguments": {
    "positions": [
      {
        "asset": "BTC",
        "value": 50000,
        "daily_returns": [0.02, -0.01, 0.03, -0.04, 0.01, -0.02, 0.005]
      },
      {
        "asset": "ETH",
        "value": 20000,
        "daily_returns": [0.015, -0.008, 0.025, -0.035, 0.012, -0.018, 0.004]
      }
    ],
    "holding_period_days": 1,
    "confidence_levels": [0.95, 0.99]
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "value_at_risk"`.
