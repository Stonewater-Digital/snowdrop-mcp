---
skill: debt_issuance_analyzer
category: capital_markets
description: Computes net proceeds, OID yields, and all-in borrowing costs for bond deals.
tier: free
inputs: face_value, coupon_rate, maturity_years, issue_price_pct, underwriter_spread_pct, rating_agency_fees, legal_fees, sec_fees
---

# Debt Issuance Analyzer

## Description
Computes net proceeds, OID yields, and all-in borrowing costs for bond deals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `face_value` | `number` | Yes |  |
| `coupon_rate` | `number` | Yes |  |
| `maturity_years` | `integer` | Yes |  |
| `issue_price_pct` | `number` | Yes |  |
| `underwriter_spread_pct` | `number` | Yes |  |
| `rating_agency_fees` | `number` | Yes |  |
| `legal_fees` | `number` | Yes |  |
| `sec_fees` | `number` | Yes |  |

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
    "face_value": 0,
    "coupon_rate": 0,
    "maturity_years": 0,
    "issue_price_pct": 0,
    "underwriter_spread_pct": 0,
    "rating_agency_fees": 0,
    "legal_fees": 0,
    "sec_fees": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "debt_issuance_analyzer"`.
