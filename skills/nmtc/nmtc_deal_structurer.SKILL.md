---
skill: nmtc_deal_structurer
category: nmtc
description: Models NMTC leveraged structures with investor equity, leverage loans, and subsidy.
tier: free
inputs: total_project_cost, nmtc_allocation, leverage_loan_rate, qlici_loan_rate, investor_required_return
---

# Nmtc Deal Structurer

## Description
Models NMTC leveraged structures with investor equity, leverage loans, and subsidy.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_project_cost` | `number` | Yes |  |
| `nmtc_allocation` | `number` | Yes |  |
| `tax_credit_pct` | `number` | No |  |
| `leverage_loan_rate` | `number` | Yes |  |
| `qlici_loan_rate` | `number` | Yes |  |
| `cde_fee_pct` | `number` | No |  |
| `investor_required_return` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nmtc_deal_structurer",
  "arguments": {
    "total_project_cost": 0,
    "nmtc_allocation": 0,
    "leverage_loan_rate": 0,
    "qlici_loan_rate": 0,
    "investor_required_return": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nmtc_deal_structurer"`.
