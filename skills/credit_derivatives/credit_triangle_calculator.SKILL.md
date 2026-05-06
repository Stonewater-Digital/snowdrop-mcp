---
skill: credit_triangle_calculator
category: credit_derivatives
description: Applies the credit triangle (spread ≈ hazard × (1 − recovery)) to reconcile CDS quotes with implied hazard and loss metrics for a given tenor.
tier: free
inputs: spread_bp, hazard_rate, recovery_rate, tenor_years
---

# Credit Triangle Calculator

## Description
Applies the credit triangle (spread ≈ hazard × (1 − recovery)) to reconcile CDS quotes with implied hazard and loss metrics for a given tenor.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spread_bp` | `number` | Yes | Observed CDS spread in basis points. |
| `hazard_rate` | `number` | Yes | Annualized hazard rate estimate (decimal). |
| `recovery_rate` | `number` | Yes | Recovery assumption in decimal form (0-1). |
| `tenor_years` | `number` | Yes | Tenor used to convert hazard rate into cumulative probability. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_triangle_calculator",
  "arguments": {
    "spread_bp": 0,
    "hazard_rate": 0,
    "recovery_rate": 0,
    "tenor_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_triangle_calculator"`.
