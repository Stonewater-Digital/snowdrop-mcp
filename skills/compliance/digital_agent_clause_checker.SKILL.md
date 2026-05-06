---
skill: digital_agent_clause_checker
category: compliance
description: Evaluates actions against identity, spend, and communication rules. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: action_type, amount, requires_external
---

# Digital Agent Clause Checker

## Description
Evaluates actions against identity, spend, and communication rules. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action_type` | `string` | Yes | The action being evaluated (e.g., "spend", "communicate", "identity_claim") |
| `amount` | `number` | Yes | Dollar amount of the action being evaluated |
| `requires_external` | `boolean` | Yes | Whether the action requires an external party or system |
| `total_assets` | `number` | No | Total assets under management for proportionality checks |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "digital_agent_clause_checker",
  "arguments": {
    "action_type": "spend",
    "amount": 5000.00,
    "requires_external": true,
    "total_assets": 2000000.00
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "digital_agent_clause_checker"`.
