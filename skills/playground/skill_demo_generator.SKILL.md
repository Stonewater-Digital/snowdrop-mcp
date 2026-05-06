---
skill: skill_demo_generator
category: playground
description: Creates narrative demo content, sample IO, and use cases for any skill.
tier: free
inputs: skill_name, skill_meta, audience
---

# Skill Demo Generator

## Description
Creates narrative demo content, sample IO, and use cases for any skill.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_name` | `string` | Yes |  |
| `skill_meta` | `object` | Yes |  |
| `audience` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_demo_generator",
  "arguments": {
    "skill_name": "<skill_name>",
    "skill_meta": {},
    "audience": "<audience>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_demo_generator"`.
