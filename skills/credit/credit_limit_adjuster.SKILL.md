---
skill: credit_limit_adjuster
category: credit
description: Applies utilization and score rules to tab limit changes.
tier: free
inputs: agent_id, current_limit, credit_score, utilization_pct, months_since_last_review
---

# Credit Limit Adjuster

## Description
Applies utilization and score rules to tab limit changes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `current_limit` | `number` | Yes |  |
| `credit_score` | `integer` | Yes |  |
| `utilization_pct` | `number` | Yes |  |
| `months_since_last_review` | `integer` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_limit_adjuster",
  "arguments": {
    "agent_id": "<agent_id>",
    "current_limit": 0,
    "credit_score": 0,
    "utilization_pct": 0,
    "months_since_last_review": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_limit_adjuster"`.
