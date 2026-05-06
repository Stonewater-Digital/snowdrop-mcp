---
skill: skill_search_engine
category: search
description: Ranks skills by textual similarity to a query string.
tier: free
inputs: query, skill_catalog
---

# Skill Search Engine

## Description
Ranks skills by textual similarity to a query string.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `query` | `string` | Yes |  |
| `skill_catalog` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_search_engine",
  "arguments": {
    "query": "<query>",
    "skill_catalog": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_search_engine"`.
