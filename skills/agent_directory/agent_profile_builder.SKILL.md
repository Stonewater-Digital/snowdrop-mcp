---
skill: agent_profile_builder
category: agent_directory
description: Creates shareable markdown pages summarizing an agent's public metrics.
tier: free
inputs: agent_id, stats, bio, showcase_skills
---

# Agent Profile Builder

## Description
Creates shareable markdown pages summarizing an agent's public metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `agent_id` | `string` | Yes |  |
| `stats` | `object` | Yes |  |
| `bio` | `string` | Yes |  |
| `showcase_skills` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_profile_builder",
  "arguments": {
    "agent_id": "<agent_id>",
    "stats": {},
    "bio": "<bio>",
    "showcase_skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_profile_builder"`.
