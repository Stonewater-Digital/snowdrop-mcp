---
skill: credit_spread_calculator
category: private_credit
description: Computes approximate yield and spread from coupon, price, and benchmark rates.
tier: free
inputs: coupon_pct, price_pct_of_par, maturity_years, benchmark_yield_pct
---

# Credit Spread Calculator

## Description
Computes approximate yield and spread from coupon, price, and benchmark rates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `coupon_pct` | `number` | Yes |  |
| `price_pct_of_par` | `number` | Yes |  |
| `maturity_years` | `number` | Yes |  |
| `benchmark_yield_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_spread_calculator",
  "arguments": {
    "coupon_pct": 0,
    "price_pct_of_par": 0,
    "maturity_years": 0,
    "benchmark_yield_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_spread_calculator"`.
