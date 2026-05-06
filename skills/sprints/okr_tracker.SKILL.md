---
skill: okr_tracker
category: sprints
description: Calculates OKR progress, color codes, and highlights at-risk objectives.
tier: free
inputs: okrs
---

# Okr Tracker

## Description
Calculates OKR progress, color codes, and highlights at-risk objectives.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `okrs` | `array` | Yes |  |
| `quarter` | `string` | No | Quarter label (e.g., Q2-2026). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "okr_tracker",
  "arguments": {
    "okrs": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "okr_tracker"`.
