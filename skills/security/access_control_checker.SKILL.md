---
skill: access_control_checker
category: security
description: Validates tier permissions across Snowdrop skills.
tier: free
inputs: agent_id, requested_skill, agent_tier
---

# Access Control Checker

## Description
Validates tier permissions across Snowdrop skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `requested_skill` | `string` | Yes |  |
| `agent_tier` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "access_control_checker",
  "arguments": {
    "agent_id": "<agent_id>",
    "requested_skill": "<requested_skill>",
    "agent_tier": "<agent_tier>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "access_control_checker"`.
