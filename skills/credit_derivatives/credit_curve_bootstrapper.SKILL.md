---
skill: credit_curve_bootstrapper
category: credit_derivatives
description: Solves for piecewise-constant hazard rates that match CDS spreads under the ISDA standard model (premium leg equals protection leg per tenor).
tier: free
inputs: tenors_years, spreads_bp, discount_factors, recovery_rate
---

# Credit Curve Bootstrapper

## Description
Solves for piecewise-constant hazard rates that match CDS spreads under the ISDA standard model (premium leg equals protection leg per tenor).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `tenors_years` | `array` | Yes | Ascending list of CDS maturities in years. |
| `spreads_bp` | `array` | Yes | Quoted running spreads in basis points for each tenor. |
| `discount_factors` | `array` | Yes | Discount factors at each tenor from the risk-free curve. |
| `recovery_rate` | `number` | Yes | Assumed recovery rate (0-1) used across the curve. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_curve_bootstrapper",
  "arguments": {
    "tenors_years": [],
    "spreads_bp": [],
    "discount_factors": [],
    "recovery_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_curve_bootstrapper"`.
