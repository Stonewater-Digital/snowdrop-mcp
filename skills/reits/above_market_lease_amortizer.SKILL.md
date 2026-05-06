---
skill: above_market_lease_amortizer
category: reits
description: Calculates periodic amortization expense for lease intangibles.
tier: free
inputs: intangible_value, remaining_term_years
---

# Above Market Lease Amortizer

## Description
Calculates periodic amortization expense for lease intangibles.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `intangible_value` | `number` | Yes |  |
| `remaining_term_years` | `number` | Yes |  |
| `discount_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "above_market_lease_amortizer",
  "arguments": {
    "intangible_value": 0,
    "remaining_term_years": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "above_market_lease_amortizer"`.
