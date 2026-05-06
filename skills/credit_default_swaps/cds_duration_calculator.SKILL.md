---
skill: cds_duration_calculator
category: credit_default_swaps
description: Calculates CDS PV01 and spread duration based on discount curve.
tier: free
inputs: notional, discount_factors, spread_bps
---

# Cds Duration Calculator

## Description
Calculates CDS PV01 and spread duration based on discount curve.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `discount_factors` | `array` | Yes |  |
| `payment_interval_years` | `number` | No |  |
| `spread_bps` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_duration_calculator",
  "arguments": {
    "notional": 0,
    "discount_factors": [],
    "spread_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_duration_calculator"`.
