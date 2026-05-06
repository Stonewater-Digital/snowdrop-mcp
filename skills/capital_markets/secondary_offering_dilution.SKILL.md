---
skill: secondary_offering_dilution
category: capital_markets
description: Evaluates dilution, proceeds, and TERP for primary/secondary offerings.
tier: free
inputs: current_shares, current_price, new_shares, offering_price, is_primary, is_secondary
---

# Secondary Offering Dilution

## Description
Evaluates dilution percentage, net proceeds, and theoretical ex-rights price (TERP) for equity follow-on offerings. Handles primary offerings (new share issuance) and secondary offerings (selling shareholder overhang) and computes EPS dilution impact.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_shares` | `integer` | Yes | Shares outstanding before the offering. |
| `current_price` | `number` | Yes | Current market price per share (dollars). |
| `new_shares` | `integer` | Yes | Number of shares being offered. |
| `offering_price` | `number` | Yes | Offering price per share (dollars). |
| `is_primary` | `boolean` | Yes | True if new shares are being issued by the company. |
| `is_secondary` | `boolean` | Yes | True if existing shareholders are selling (creates overhang but no dilution). |
| `underwriter_discount_pct` | `number` | No | Gross underwriter spread as a percentage (default: 5.0). |

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
    "current_shares": 100000000,
    "current_price": 45.50,
    "new_shares": 8000000,
    "offering_price": 43.00,
    "is_primary": true,
    "is_secondary": false,
    "underwriter_discount_pct": 4.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "secondary_offering_dilution"`.
