---
skill: ipo_pricing_analyzer
category: capital_markets
description: Evaluates implied valuation, dilution, and discount to comps for IPO ranges.
tier: free
inputs: filing_range_low, filing_range_high, shares_offered, pre_ipo_shares, comps, company_revenue, company_ebitda
---

# IPO Pricing Analyzer

## Description
Evaluates implied valuation, dilution, and discount to comps for IPO pricing ranges. Computes implied enterprise value across the filing range, dilution percentage, gross proceeds with greenshoe, discount or premium to comparable company multiples, and a first-day pop estimate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `filing_range_low` | `number` | Yes | Low end of the IPO price range (dollars per share). |
| `filing_range_high` | `number` | Yes | High end of the IPO price range (dollars per share). |
| `shares_offered` | `integer` | Yes | Number of new shares being offered in the IPO. |
| `pre_ipo_shares` | `integer` | Yes | Total shares outstanding before the offering. |
| `comps` | `array` | Yes | List of comparable company objects, each with an `ev_revenue` field. |
| `company_revenue` | `number` | Yes | Issuer trailing or forward revenue (dollars). |
| `company_ebitda` | `number` | Yes | Issuer trailing or forward EBITDA (dollars). |
| `greenshoe_pct` | `number` | No | Overallotment option size as a percentage of shares offered (default: 15.0). |

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
    "filing_range_low": 18.00,
    "filing_range_high": 21.00,
    "shares_offered": 10000000,
    "pre_ipo_shares": 80000000,
    "comps": [
      {"name": "CompA", "ev_revenue": 4.5},
      {"name": "CompB", "ev_revenue": 5.2}
    ],
    "company_revenue": 350000000,
    "company_ebitda": 42000000,
    "greenshoe_pct": 15.0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ipo_pricing_analyzer"`.
