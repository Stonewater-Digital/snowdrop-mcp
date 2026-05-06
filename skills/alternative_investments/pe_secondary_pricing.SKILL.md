---
skill: pe_secondary_pricing
category: alternative_investments
description: Applies secondary market heuristics (quartile + remaining commitment) to derive bid discount and implied IRR.
tier: premium
inputs: nav, remaining_commitment, fund_age_years, fund_quartile, j_curve_position
---

# PE Secondary Pricing

## Description
Applies secondary market heuristics based on fund quartile ranking, remaining unfunded commitment, and J-curve position to derive a bid discount to NAV and implied secondary buyer IRR. Useful for pricing LP interest sales and secondary market portfolio construction. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `nav` | `number` | Yes | Current net asset value of the LP interest (dollars). |
| `remaining_commitment` | `number` | Yes | Unfunded remaining commitment (dollars). |
| `fund_age_years` | `number` | Yes | Age of the fund in years from first close. |
| `fund_quartile` | `integer` | Yes | Fund performance quartile: 1 (top) through 4 (bottom). |
| `j_curve_position` | `number` | Yes | J-curve position as a fraction of typical drawdown period (0.0 = start, 1.0 = inflection). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "pe_secondary_pricing",
  "arguments": {
    "nav": 50000000,
    "remaining_commitment": 8000000,
    "fund_age_years": 6.5,
    "fund_quartile": 2,
    "j_curve_position": 0.75
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pe_secondary_pricing"`.
