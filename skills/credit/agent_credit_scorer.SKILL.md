---
skill: agent_credit_scorer
category: credit
description: Generates 300-850 style scores using payment history and utilization inputs.
tier: free
inputs: agent_id, account_age_days, payment_history, current_tab, tier
---

# Agent Credit Scorer

## Description
Generates 300-850 style scores using payment history and utilization inputs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `account_age_days` | `integer` | Yes |  |
| `payment_history` | `array` | Yes |  |
| `current_tab` | `number` | Yes |  |
| `tier` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_credit_scorer",
  "arguments": {
    "agent_id": "<agent_id>",
    "account_age_days": 0,
    "payment_history": [],
    "current_tab": 0,
    "tier": "<tier>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_credit_scorer"`.
