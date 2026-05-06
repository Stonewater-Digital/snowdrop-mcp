---
skill: annuity_pricing_tool
category: insurance_analytics
description: Prices whole-life and deferred-life annuities-due using a simple mortality model calibrated to approximate 2017 CSO rates. Returns annuity factor, present value, and break-even analysis metrics.
tier: free
inputs: age, gender, discount_rate_pct
---

# Annuity Pricing Tool

## Description
Prices whole-life and deferred-life annuities-due using a simple mortality model calibrated to approximate 2017 CSO rates. Returns annuity factor, present value, and break-even analysis metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `age` | `integer` | Yes | Annuitant's current attained age. Must be 0–100. |
| `gender` | `string` | Yes | Gender for mortality curve selection. |
| `discount_rate_pct` | `number` | Yes | Annual discount rate as a percentage (e.g., 4.0 = 4.0%). Must be >= 0. |
| `payment_amount` | `number` | No | Annual payment amount per period. Must be > 0. |
| `annuity_type` | `string` | No | Annuity-immediate starts next period; deferred starts after deferral_years. |
| `deferral_years` | `integer` | No | Years before first payment for a deferred annuity. Must be >= 0. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "annuity_pricing_tool",
  "arguments": {
    "age": 0,
    "gender": "<gender>",
    "discount_rate_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "annuity_pricing_tool"`.
