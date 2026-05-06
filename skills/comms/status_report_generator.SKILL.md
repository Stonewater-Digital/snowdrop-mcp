---
skill: status_report_generator
category: comms
description: Formats Snowdrop execution updates into a markdown status report.
tier: free
inputs: completed, in_progress, blocked, metrics, highlights, period
---

# Status Report Generator

## Description
Formats Snowdrop execution updates into a markdown status report.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `completed` | `array` | Yes |  |
| `in_progress` | `array` | Yes |  |
| `blocked` | `array` | Yes |  |
| `metrics` | `object` | Yes |  |
| `highlights` | `array` | Yes |  |
| `period` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "status_report_generator",
  "arguments": {
    "completed": [],
    "in_progress": [],
    "blocked": [],
    "metrics": {},
    "highlights": [],
    "period": "<period>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "status_report_generator"`.
