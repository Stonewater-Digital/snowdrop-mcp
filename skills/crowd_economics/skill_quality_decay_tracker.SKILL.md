---
skill: skill_quality_decay_tracker
category: crowd_economics
description: Measures error rate drift and maintenance burden for community skills over time.
tier: free
inputs: skill_snapshots
---

# Skill Quality Decay Tracker

## Description
Measures error rate drift and maintenance burden for community skills over time.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_snapshots` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_quality_decay_tracker",
  "arguments": {
    "skill_snapshots": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_quality_decay_tracker"`.
