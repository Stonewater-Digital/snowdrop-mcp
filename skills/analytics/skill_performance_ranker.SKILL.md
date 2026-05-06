---
skill: skill_performance_ranker
category: analytics
description: Combines reliability, latency, popularity, and satisfaction into a composite score.
tier: free
inputs: skill_metrics
---

# Skill Performance Ranker

## Description
Combines reliability, latency, popularity, and satisfaction into a composite score.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_metrics` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skill_performance_ranker",
  "arguments": {
    "skill_metrics": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skill_performance_ranker"`.
