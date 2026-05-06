---
skill: community_skill_adoption_tracker
category: crowd_economics
description: Compares usage, revenue, and growth metrics between internal and community skills.
tier: free
inputs: skills
---

# Community Skill Adoption Tracker

## Description
Compares usage, revenue, and growth metrics between internal and community skills.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skills` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "community_skill_adoption_tracker",
  "arguments": {
    "skills": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "community_skill_adoption_tracker"`.
