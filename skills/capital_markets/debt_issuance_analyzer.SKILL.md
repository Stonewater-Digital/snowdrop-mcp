---
skill: debt_issuance_analyzer
category: capital_markets
description: Computes net proceeds, OID yields, and all-in borrowing costs for bond deals.
tier: free
inputs: face_value, coupon_rate, maturity_years, issue_price_pct, underwriter_spread_pct, rating_agency_fees, legal_fees, sec_fees
---

# Debt Issuance Analyzer

## Description
Computes net proceeds, original issue discount (OID) amortization, and all-in borrowing cost for a bond issuance. Aggregates underwriter spread, rating agency fees, legal costs, and SEC registration fees into a single effective cost metric and benchmarks it against the stated coupon.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `face_value` | `number` | Yes | Total face value (principal) of the bond issuance (dollars). |
| `coupon_rate` | `number` | Yes | Annual coupon rate as a decimal (e.g. 0.055 for 5.5%). |
| `maturity_years` | `integer` | Yes | Term of the bond in years. |
| `issue_price_pct` | `number` | Yes | Issue price as a percentage of par (e.g. 99.5 for a slight discount). |
| `underwriter_spread_pct` | `number` | Yes | Underwriter gross spread as a percentage of face value. |
| `rating_agency_fees` | `number` | Yes | Total rating agency fees (dollars). |
| `legal_fees` | `number` | Yes | Legal and counsel fees (dollars). |
| `sec_fees` | `number` | Yes | SEC registration and filing fees (dollars). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "debt_issuance_analyzer",
  "arguments": {
    "face_value": 500000000,
    "coupon_rate": 0.055,
    "maturity_years": 10,
    "issue_price_pct": 99.5,
    "underwriter_spread_pct": 0.875,
    "rating_agency_fees": 300000,
    "legal_fees": 1200000,
    "sec_fees": 65000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_issuance_analyzer"`.
