---
skill: paycheck_calculator
category: personal_finance
description: Calculate net take-home pay from gross pay after federal, state, and FICA taxes. Supports multiple pay frequencies.
tier: free
inputs: gross_pay
---

# Paycheck Calculator

## Description
Calculate net take-home pay from gross pay after federal, state, and FICA taxes. Supports multiple pay frequencies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_pay` | `number` | Yes | Gross pay per pay period. |
| `pay_frequency` | `string` | No | Pay frequency: 'weekly', 'biweekly', 'semimonthly', 'monthly'. |
| `federal_rate` | `number` | No | Effective federal income tax rate as decimal (e.g., 0.22 for 22%). |
| `state_rate` | `number` | No | Effective state income tax rate as decimal (e.g., 0.05 for 5%). |
| `fica_rate` | `number` | No | FICA rate as decimal (Social Security 6.2% + Medicare 1.45% = 7.65%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "paycheck_calculator",
  "arguments": {
    "gross_pay": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "paycheck_calculator"`.
