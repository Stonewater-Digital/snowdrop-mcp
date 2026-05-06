---
skill: cet1_deduction_engine
category: regulatory_capital
description: Computes CET1 deductions with 15% aggregate threshold for DTAs, MSRs, and investments.
tier: free
inputs: goodwill, deferred_tax_assets, mortgage_servicing_rights, significant_investments, cet1_before_deductions
---

# Cet1 Deduction Engine

## Description
Computes CET1 deductions with 15% aggregate threshold for DTAs, MSRs, and investments.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `goodwill` | `number` | Yes | Goodwill net of deferred tax liabilities. |
| `deferred_tax_assets` | `number` | Yes | DTAs arising from temporary differences. |
| `mortgage_servicing_rights` | `number` | Yes | MSRs amount. |
| `significant_investments` | `number` | Yes | Significant investments in financial sector entities. |
| `cet1_before_deductions` | `number` | Yes | CET1 before regulatory deductions. |
| `threshold_limits` | `object` | No | Threshold percentages (e.g., 10%, 15%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cet1_deduction_engine",
  "arguments": {
    "goodwill": 0,
    "deferred_tax_assets": 0,
    "mortgage_servicing_rights": 0,
    "significant_investments": 0,
    "cet1_before_deductions": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cet1_deduction_engine"`.
