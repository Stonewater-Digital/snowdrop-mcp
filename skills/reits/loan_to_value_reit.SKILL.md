---
skill: loan_to_value_reit
category: reits
description: Calculates gross and net loan-to-value ratios for REIT balance sheets.
tier: free
inputs: total_debt, gross_asset_value
---

# Loan To Value Reit

## Description
Calculates gross and net loan-to-value ratios for REIT balance sheets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_debt` | `number` | Yes |  |
| `gross_asset_value` | `number` | Yes |  |
| `cash_and_restricted` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_to_value_reit",
  "arguments": {
    "total_debt": 0,
    "gross_asset_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_to_value_reit"`.
