---
skill: three_statement_modeler
category: budgeting
description: Generates linked financial statements using indirect cash flow method.
tier: free
inputs: income_statement, prior_balance_sheet, assumptions
---

# Three Statement Modeler

## Description
Generates linked financial statements using indirect cash flow method.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `income_statement` | `object` | Yes |  |
| `prior_balance_sheet` | `object` | Yes |  |
| `assumptions` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "three_statement_modeler",
  "arguments": {
    "income_statement": {},
    "prior_balance_sheet": {},
    "assumptions": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "three_statement_modeler"`.
