---
skill: gross_to_net_calculator
category: payroll
description: Calculate net (take-home) pay from gross pay after federal tax, state tax, FICA, and pre-tax deductions.
tier: free
inputs: gross_pay
---

# Gross To Net Calculator

## Description
Calculate net (take-home) pay from gross pay after federal tax, state tax, FICA, and pre-tax deductions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_pay` | `number` | Yes | Gross pay for the period in USD. |
| `federal_rate` | `number` | No | Effective federal tax rate as a decimal. |
| `state_rate` | `number` | No | State income tax rate as a decimal. |
| `fica_rate` | `number` | No | FICA rate (Social Security + Medicare) as a decimal. |
| `pre_tax_deductions` | `number` | No | Pre-tax deductions (401k, HSA, health insurance, etc.) in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gross_to_net_calculator",
  "arguments": {
    "gross_pay": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gross_to_net_calculator"`.
