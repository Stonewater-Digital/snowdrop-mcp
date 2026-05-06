---
skill: blue_sky_filing_fee_calculator
category: securities_tax
description: Calculates blue sky filing fees using schedule caps and minimums.
tier: free
inputs: offering_amount, states
---

# Blue Sky Filing Fee Calculator

## Description
Calculates blue sky filing fees using schedule caps and minimums.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `offering_amount` | `number` | Yes |  |
| `states` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "blue_sky_filing_fee_calculator",
  "arguments": {
    "offering_amount": 0,
    "states": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "blue_sky_filing_fee_calculator"`.
