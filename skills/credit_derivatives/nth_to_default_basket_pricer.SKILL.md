---
skill: nth_to_default_basket_pricer
category: credit_derivatives
description: Monte Carlo Gaussian copula model (Li, 2000) for nth-to-default baskets with systematic correlation and discounted loss metrics.
tier: free
inputs: default_probabilities, pairwise_correlation, recovery_rate, notional, nth, horizon_years, discount_rate, num_paths
---

# Nth To Default Basket Pricer

## Description
Monte Carlo Gaussian copula model (Li, 2000) for nth-to-default baskets with systematic correlation and discounted loss metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `default_probabilities` | `array` | Yes | Marginal default probabilities over the horizon for each reference obligor. |
| `pairwise_correlation` | `number` | Yes | Asset correlation applied uniformly across the basket. |
| `recovery_rate` | `number` | Yes | Expected recovery rate applied to each obligor (0-1). |
| `notional` | `number` | Yes | Tranche notional in currency units. |
| `nth` | `integer` | Yes | Order of default that triggers the tranche. |
| `horizon_years` | `number` | Yes | Tenor of the basket in years. |
| `discount_rate` | `number` | Yes | Continuous risk-free discount rate for PV calculations. |
| `num_paths` | `integer` | Yes | Monte Carlo path count (>=2000 recommended). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nth_to_default_basket_pricer",
  "arguments": {
    "default_probabilities": [],
    "pairwise_correlation": 0,
    "recovery_rate": 0,
    "notional": 0,
    "nth": 0,
    "horizon_years": 0,
    "discount_rate": 0,
    "num_paths": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nth_to_default_basket_pricer"`.
