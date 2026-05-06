---
skill: usage_heatmap_generator
category: analytics
description: Buckets skill requests into hour/day heatmap bins for usage insights.
tier: free
inputs: requests
---

# Usage Heatmap Generator

## Description
Buckets skill requests into hour/day heatmap bins for usage insights.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `requests` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "usage_heatmap_generator",
  "arguments": {
    "requests": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "usage_heatmap_generator"`.
