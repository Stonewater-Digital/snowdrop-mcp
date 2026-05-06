---
skill: fsa_usage_planner
category: personal_finance
description: Plan Flexible Spending Account (FSA) usage by comparing annual contribution against expected expenses. Identifies surplus risk under the use-it-or-lose-it rule.
tier: free
inputs: annual_contribution, expected_expenses
---

# Fsa Usage Planner

## Description
Plan Flexible Spending Account (FSA) usage by comparing annual contribution against expected expenses. Identifies surplus risk under the use-it-or-lose-it rule.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `annual_contribution` | `number` | Yes | Annual FSA contribution amount. |
| `expected_expenses` | `array` | Yes | List of expected medical/dependent care expenses with category and amount. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fsa_usage_planner",
  "arguments": {
    "annual_contribution": 0,
    "expected_expenses": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fsa_usage_planner"`.
