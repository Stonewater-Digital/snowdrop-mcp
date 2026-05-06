---
skill: community_skill_submitter
category: skill_marketplace
description: Validates community skill code before it enters the review queue.
tier: free
inputs: agent_id, skill_name, skill_code, description, category, requested_price
---

# Community Skill Submitter

## Description
Validates community skill code before it enters the review queue.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `skill_name` | `string` | Yes |  |
| `skill_code` | `string` | Yes |  |
| `description` | `string` | Yes |  |
| `category` | `string` | Yes |  |
| `requested_price` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "community_skill_submitter",
  "arguments": {
    "agent_id": "<agent_id>",
    "skill_name": "<skill_name>",
    "skill_code": "<skill_code>",
    "description": "<description>",
    "category": "<category>",
    "requested_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "community_skill_submitter"`.
