---
skill: gradual_rollout_controller
category: feature_mgmt
description: Decides if an agent is part of a canary rollout using deterministic hashing.
tier: free
inputs: skill_name, rollout_pct, agent_id
---

# Gradual Rollout Controller

## Description
Decides if an agent is part of a canary rollout using deterministic hashing.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_name` | `string` | Yes |  |
| `rollout_pct` | `number` | Yes |  |
| `agent_id` | `string` | Yes |  |
| `population_size` | `integer` | No | Optional population estimate for reporting. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "gradual_rollout_controller",
  "arguments": {
    "skill_name": "<skill_name>",
    "rollout_pct": 0,
    "agent_id": "<agent_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gradual_rollout_controller"`.
