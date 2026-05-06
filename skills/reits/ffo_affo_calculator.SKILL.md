---
skill: ffo_affo_calculator
category: reits
description: Calculates FFO/AFFO and payout ratios for REITs.
tier: free
inputs: net_income, depreciation_real_estate, amortization_real_estate, gains_on_sale, losses_on_sale, impairments, straight_line_rent_adj, recurring_capex, lease_commissions, tenant_improvements, shares_outstanding
---

# Ffo Affo Calculator

## Description
Calculates FFO/AFFO and payout ratios for REITs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_income` | `number` | Yes |  |
| `depreciation_real_estate` | `number` | Yes |  |
| `amortization_real_estate` | `number` | Yes |  |
| `gains_on_sale` | `number` | Yes |  |
| `losses_on_sale` | `number` | Yes |  |
| `impairments` | `number` | Yes |  |
| `straight_line_rent_adj` | `number` | Yes |  |
| `recurring_capex` | `number` | Yes |  |
| `lease_commissions` | `number` | Yes |  |
| `tenant_improvements` | `number` | Yes |  |
| `shares_outstanding` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ffo_affo_calculator",
  "arguments": {
    "net_income": 0,
    "depreciation_real_estate": 0,
    "amortization_real_estate": 0,
    "gains_on_sale": 0,
    "losses_on_sale": 0,
    "impairments": 0,
    "straight_line_rent_adj": 0,
    "recurring_capex": 0,
    "lease_commissions": 0,
    "tenant_improvements": 0,
    "shares_outstanding": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ffo_affo_calculator"`.
