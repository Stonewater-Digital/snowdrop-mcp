---
skill: child_tax_credit_calculator
category: tax
description: Calculate the Child Tax Credit ($2,000 per child under 17) with income phase-out at $200k single / $400k MFJ. $50 reduction per $1,000 over threshold.
tier: free
inputs: num_children_under_17, agi
---

# Child Tax Credit Calculator

## Description
Calculate the Child Tax Credit ($2,000 per child under 17) with income phase-out at $200k single / $400k MFJ. $50 reduction per $1,000 over threshold.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `num_children_under_17` | `integer` | Yes | Number of qualifying children under age 17. |
| `agi` | `number` | Yes | Adjusted gross income in USD. |
| `filing_status` | `string` | No | Filing status. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "child_tax_credit_calculator",
  "arguments": {
    "num_children_under_17": 0,
    "agi": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "child_tax_credit_calculator"`.
