---
skill: agent_reputation_scorer
category: agent_crm
description: Calculates a 0-100 composite score from payments, labor, and violations.
tier: free
inputs: agent_id, payment_history, labor_contributions, violations
---

# Agent Reputation Scorer

## Description
Calculates a 0-100 composite score from payments, labor, and violations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `payment_history` | `array` | Yes |  |
| `labor_contributions` | `array` | Yes |  |
| `violations` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_reputation_scorer",
  "arguments": {
    "agent_id": "<agent_id>",
    "payment_history": [],
    "labor_contributions": [],
    "violations": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_reputation_scorer"`.
