---
skill: post_mortem_generator
category: incidents
description: Creates structured post-mortem Markdown with action items and lessons learned.
tier: free
inputs: incident
---

# Post Mortem Generator

## Description
Creates structured post-mortem Markdown with action items and lessons learned.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `incident` | `object` | Yes | Incident dictionary containing title, severity, timeline, root cause, contributing factors, detection_method, resolution, and duration_minutes. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "post_mortem_generator",
  "arguments": {
    "incident": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "post_mortem_generator"`.
