---
skill: value_at_risk_montecarlo
category: market_analytics
description: Simulates returns via a Gaussian process to estimate VaR and expected shortfall.
tier: free
inputs: mean_return, volatility, num_simulations, confidence_level, horizon_days
---

# Value At Risk Montecarlo

## Description
Simulates returns via a Gaussian process to estimate VaR and expected shortfall.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mean_return` | `number` | Yes | Expected daily return (decimal). |
| `volatility` | `number` | Yes | Daily volatility (standard deviation). |
| `num_simulations` | `integer` | Yes | Number of Monte Carlo paths. |
| `confidence_level` | `number` | Yes | Confidence level between 0 and 1. |
| `horizon_days` | `integer` | Yes | Holding period in days. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "value_at_risk_montecarlo",
  "arguments": {
    "mean_return": 0,
    "volatility": 0,
    "num_simulations": 0,
    "confidence_level": 0,
    "horizon_days": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "value_at_risk_montecarlo"`.
