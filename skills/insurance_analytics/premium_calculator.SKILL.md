---
skill: premium_calculator
category: insurance_analytics
description: Computes gross written premium from base rate, exposure units, experience modification, schedule credits, and other adjustments following standard manual rating methodology.
tier: free
inputs: base_rate, exposure_units
---

# Premium Calculator

## Description
Computes gross written premium from base rate, exposure units, experience modification, schedule credits, and other adjustments following standard manual rating methodology.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_rate` | `number` | Yes | Base rate per exposure unit (e.g., dollars per $100 of payroll, per vehicle, per unit). |
| `exposure_units` | `number` | Yes | Number of exposure units (e.g., payroll in $100s, vehicle count, headcount). |
| `experience_mod` | `number` | No | Experience modification factor (e-mod). 1.0 = unity; <1.0 = credit; >1.0 = debit. Typical range 0.50–2.50. |
| `schedule_credits_pct` | `number` | No | Schedule rating adjustment as a signed percentage of experience-adjusted premium. Positive = surcharge, negative = credit. Most states cap at ±25%. |
| `other_adjustments_pct` | `number` | No | Additional multiplicative adjustment as a signed percentage (e.g., premium discount, expense constant). Applied after schedule factor. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "premium_calculator",
  "arguments": {
    "base_rate": 0,
    "exposure_units": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "premium_calculator"`.
