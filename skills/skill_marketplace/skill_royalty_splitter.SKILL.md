---
skill: skill_royalty_splitter
category: skill_marketplace
description: Calculates revenue splits for community skills and tracks contributor balances.
tier: free
inputs: skill_name, revenue, contributor_id
---

# Skill Royalty Splitter

## Description
Calculates revenue splits for community skills and tracks contributor balances.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_name` | `string` | Yes |  |
| `revenue` | `number` | Yes |  |
| `contributor_id` | `string` | Yes |  |
| `platform_rate_pct` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_royalty_splitter",
  "arguments": {
    "skill_name": "<skill_name>",
    "revenue": 0,
    "contributor_id": "<contributor_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_royalty_splitter"`.
