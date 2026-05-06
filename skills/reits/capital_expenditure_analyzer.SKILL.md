---
skill: capital_expenditure_analyzer
category: reits
description: Breaks capex into maintenance vs growth and measures NOI burden.
tier: free
inputs: maintenance_capex, growth_capex, net_operating_income
---

# Capital Expenditure Analyzer

## Description
Breaks capex into maintenance vs growth and measures NOI burden.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `maintenance_capex` | `number` | Yes |  |
| `growth_capex` | `number` | Yes |  |
| `net_operating_income` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "capital_expenditure_analyzer",
  "arguments": {
    "maintenance_capex": 0,
    "growth_capex": 0,
    "net_operating_income": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "capital_expenditure_analyzer"`.
