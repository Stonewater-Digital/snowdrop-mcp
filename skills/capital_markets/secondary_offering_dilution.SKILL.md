---
skill: secondary_offering_dilution
category: capital_markets
description: Evaluates dilution, proceeds, and TERP for primary/secondary offerings.
tier: free
inputs: current_shares, current_price, new_shares, offering_price, is_primary, is_secondary
---

# Secondary Offering Dilution

## Description
Evaluates dilution, proceeds, and TERP for primary/secondary offerings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_shares` | `integer` | Yes |  |
| `current_price` | `number` | Yes |  |
| `new_shares` | `integer` | Yes |  |
| `offering_price` | `number` | Yes |  |
| `is_primary` | `boolean` | Yes |  |
| `is_secondary` | `boolean` | Yes |  |
| `underwriter_discount_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "secondary_offering_dilution",
  "arguments": {
    "current_shares": 0,
    "current_price": 0,
    "new_shares": 0,
    "offering_price": 0,
    "is_primary": false,
    "is_secondary": false
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "secondary_offering_dilution"`.
