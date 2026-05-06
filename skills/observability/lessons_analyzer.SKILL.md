---
skill: lessons_analyzer
category: observability
description: Parses logs/lessons.md content for failure hotspots and trends.
tier: free
inputs: lessons_content
---

# Lessons Analyzer

## Description
Parses logs/lessons.md content for failure hotspots and trends.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `lessons_content` | `string` | Yes |  |
| `time_range_hours` | `['integer', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "lessons_analyzer",
  "arguments": {
    "lessons_content": "<lessons_content>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lessons_analyzer"`.
