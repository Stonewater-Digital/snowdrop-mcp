---
skill: cds_upfront_to_running_converter
category: credit_default_swaps
description: Converts CDS upfront percentage into equivalent running spread.
tier: free
inputs: notional, upfront_pct, risky_annuity
---

# Cds Upfront To Running Converter

## Description
Converts CDS upfront percentage into equivalent running spread.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `upfront_pct` | `number` | Yes |  |
| `risky_annuity` | `number` | Yes |  |
| `coupon_bps` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_upfront_to_running_converter",
  "arguments": {
    "notional": 0,
    "upfront_pct": 0,
    "risky_annuity": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_upfront_to_running_converter"`.
