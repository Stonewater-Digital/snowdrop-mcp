---
skill: proforma_generator
category: real_estate_finance
description: Projects multi-year cash flows, NOI, and returns for income properties.
tier: free
inputs: purchase_price, gross_potential_rent_annual, exit_cap_rate
---

# Proforma Generator

## Description
Projects multi-year cash flows, NOI, and returns for income properties.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `purchase_price` | `number` | Yes |  |
| `units` | `integer` | No |  |
| `gross_potential_rent_annual` | `number` | Yes |  |
| `vacancy_rate_pct` | `number` | No |  |
| `operating_expense_ratio_pct` | `number` | No |  |
| `capex_reserve_pct` | `number` | No |  |
| `loan` | `object` | No |  |
| `hold_period_years` | `integer` | No |  |
| `rent_growth_pct` | `number` | No |  |
| `exit_cap_rate` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "proforma_generator",
  "arguments": {
    "purchase_price": 0,
    "gross_potential_rent_annual": 0,
    "exit_cap_rate": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "proforma_generator"`.
