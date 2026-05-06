---
skill: skill_catalog_sync
category: skillmeta
description: Returns live skill count breakdown (total, free, premium, failed) from the running server. Pass regenerate=True to rebuild SNOWDROP_SKILLS.md and SKILLS.md from the current codebase (admin use only).
tier: free
inputs: none
---

# Skill Catalog Sync

## Description
Returns live skill count breakdown (total, free, premium, failed) from the running server. Pass regenerate=True to rebuild SNOWDROP_SKILLS.md and SKILLS.md from the current codebase (admin use only).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `regenerate` | `boolean` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_catalog_sync",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_catalog_sync"`.
