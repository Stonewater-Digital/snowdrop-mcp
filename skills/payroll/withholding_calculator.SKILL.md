---
skill: withholding_calculator
category: payroll
description: Calculate federal income tax withholding per pay period by annualizing gross pay, applying 2024 tax brackets, and dividing back to per-period amounts.
tier: free
inputs: gross_pay
---

# Withholding Calculator

## Description
Calculate federal income tax withholding per pay period by annualizing gross pay, applying 2024 tax brackets, and dividing back to per-period amounts.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_pay` | `number` | Yes | Gross pay for the period in USD. |
| `pay_period` | `string` | No | Pay period frequency. |
| `w4_filing_status` | `string` | No | W-4 filing status. |
| `allowances` | `integer` | No | Number of withholding allowances (pre-2020 W-4 style). Each reduces taxable by ~$4,300. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "withholding_calculator",
  "arguments": {
    "gross_pay": 3846.15
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "withholding_calculator"`.
