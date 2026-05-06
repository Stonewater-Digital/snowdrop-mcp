---
skill: ipo_pricing_analyzer
category: capital_markets
description: Evaluates implied valuation, dilution, and discount to comps for IPO ranges.
tier: free
inputs: filing_range_low, filing_range_high, shares_offered, pre_ipo_shares, comps, company_revenue, company_ebitda
---

# Ipo Pricing Analyzer

## Description
Evaluates implied valuation, dilution, and discount to comps for IPO ranges.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `filing_range_low` | `number` | Yes |  |
| `filing_range_high` | `number` | Yes |  |
| `shares_offered` | `integer` | Yes |  |
| `pre_ipo_shares` | `integer` | Yes |  |
| `greenshoe_pct` | `number` | No |  |
| `comps` | `array` | Yes |  |
| `company_revenue` | `number` | Yes |  |
| `company_ebitda` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ipo_pricing_analyzer",
  "arguments": {
    "filing_range_low": 0,
    "filing_range_high": 0,
    "shares_offered": 0,
    "pre_ipo_shares": 0,
    "comps": [],
    "company_revenue": 0,
    "company_ebitda": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ipo_pricing_analyzer"`.
