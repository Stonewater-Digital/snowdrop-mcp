---
skill: lesson_to_action_sync_bot
category: workflow
description: Scan logs/lessons.md, cluster recurring entries, and emit recommended follow-up actions.
tier: free
inputs: none
---

# Lesson To Action Sync Bot

## Description
Scan logs/lessons.md, cluster recurring entries, and emit recommended follow-up actions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lessons_path` | `string` | No | Path to Ralph Wiggum log file. |
| `owner_map` | `object` | No | Keyword -> owner/team routing map to tag recommendations. |
| `max_items` | `integer` | No | Maximum number of action recommendations to return. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lesson_to_action_sync_bot",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lesson_to_action_sync_bot"`.
