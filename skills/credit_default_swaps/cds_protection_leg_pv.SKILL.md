---
skill: cds_protection_leg_pv
category: credit_default_swaps
description: Computes PV of CDS protection leg using default probabilities.
tier: free
inputs: notional, default_probabilities, discount_factors
---

# Cds Protection Leg Pv

## Description
Computes PV of CDS protection leg using default probabilities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `default_probabilities` | `array` | Yes |  |
| `discount_factors` | `array` | Yes |  |
| `recovery_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_protection_leg_pv",
  "arguments": {
    "notional": 0,
    "default_probabilities": [],
    "discount_factors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_protection_leg_pv"`.
