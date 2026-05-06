---
skill: net_pay_calculator
category: personal_finance
description: Calculate annual and periodic net pay from gross annual salary after federal, state, and FICA taxes and pre-tax deductions.
tier: free
inputs: gross_annual
---

# Net Pay Calculator

## Description
Calculate annual and periodic net pay from gross annual salary after federal, state, and FICA taxes and pre-tax deductions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_annual` | `number` | Yes | Gross annual salary. |
| `federal_rate` | `number` | No | Effective federal income tax rate as decimal. |
| `state_rate` | `number` | No | Effective state income tax rate as decimal. |
| `fica_rate` | `number` | No | FICA rate as decimal (SS + Medicare). |
| `deductions` | `number` | No | Annual pre-tax deductions (401k, HSA, health insurance premiums, etc.). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "net_pay_calculator",
  "arguments": {
    "gross_annual": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "net_pay_calculator"`.
