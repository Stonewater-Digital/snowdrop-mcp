---
skill: present_value_calculator
category: personal_finance
description: Computes the present value of a lump sum or annuity, adjusting for payment timing and reporting aggregate payments and implied interest.
tier: free
inputs: rate, periods, annuity_type
---

# Present Value Calculator

## Description
Computes the present value of a lump sum or annuity, adjusting for payment timing and reporting aggregate payments and implied interest.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `future_value` | `number` | No | Future lump sum value in dollars (optional). |
| `payment` | `number` | No | Recurring payment amount for annuities (optional). |
| `rate` | `number` | Yes | Periodic discount rate as decimal. |
| `periods` | `number` | Yes | Number of compounding or payment periods. |
| `annuity_type` | `string` | Yes | Payment timing: ordinary (end) or due (beginning). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "present_value_calculator",
  "arguments": {
    "rate": 0,
    "periods": 0,
    "annuity_type": "<annuity_type>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "present_value_calculator"`.
