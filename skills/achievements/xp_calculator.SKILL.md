---
skill: xp_calculator
category: achievements
description: Tallies XP from recent activities and estimates level progression.
tier: free
inputs: activities
---

# Xp Calculator

## Description
Tallies XP from recent activities and estimates level progression.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `activities` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "xp_calculator",
  "arguments": {
    "activities": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "xp_calculator"`.
