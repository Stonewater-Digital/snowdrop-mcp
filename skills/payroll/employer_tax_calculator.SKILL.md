---
skill: employer_tax_calculator
category: payroll
description: Calculate employer-side payroll taxes: employer FICA match (7.65%), FUTA (0.6% on first $7,000), and SUTA (variable on wage base).
tier: free
inputs: gross_payroll, num_employees
---

# Employer Tax Calculator

## Description
Calculate employer-side payroll taxes: employer FICA match (7.65%), FUTA (0.6% on first $7,000), and SUTA (variable on wage base).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_payroll` | `number` | Yes | Total gross payroll for the period in USD. |
| `num_employees` | `integer` | Yes | Number of employees on payroll. |
| `futa_rate` | `number` | No | FUTA tax rate as a decimal (after state credit, typically 0.006). |
| `suta_rate` | `number` | No | SUTA (state unemployment) tax rate as a decimal. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "employer_tax_calculator",
  "arguments": {
    "gross_payroll": 0,
    "num_employees": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "employer_tax_calculator"`.
