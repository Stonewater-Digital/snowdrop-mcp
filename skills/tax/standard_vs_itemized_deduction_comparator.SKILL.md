---
skill: standard_vs_itemized_deduction_comparator
category: tax
description: Compare standard deduction vs itemized deductions (mortgage interest, SALT capped at $10k, charitable, medical over 7.5% AGI) and recommend the higher deduction for 2024.
tier: free
inputs: none
---

# Standard Vs Itemized Deduction Comparator

## Description
Compare standard deduction vs itemized deductions (mortgage interest, SALT capped at $10k, charitable, medical over 7.5% AGI) and recommend the higher deduction for 2024.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `filing_status` | `string` | No | Filing status. |
| `mortgage_interest` | `number` | No | Mortgage interest paid in USD. |
| `state_local_taxes` | `number` | No | State and local taxes paid (income + property) in USD. |
| `charitable` | `number` | No | Charitable contributions in USD. |
| `medical` | `number` | No | Total medical expenses in USD. |
| `agi` | `number` | No | Adjusted gross income in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "standard_vs_itemized_deduction_comparator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "standard_vs_itemized_deduction_comparator"`.
