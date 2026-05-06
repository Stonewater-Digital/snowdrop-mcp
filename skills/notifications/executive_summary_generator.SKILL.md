---
skill: executive_summary_generator
category: notifications
description: Formats operational metrics into a Thunder-ready briefing.
tier: free
inputs: metrics
---

# Executive Summary Generator

## Description
Formats operational metrics into a Thunder-ready briefing.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `metrics` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "executive_summary_generator",
  "arguments": {
    "metrics": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "executive_summary_generator"`.
