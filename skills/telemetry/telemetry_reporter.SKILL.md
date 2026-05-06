---
skill: telemetry_reporter
category: telemetry
description: Aggregates telemetry events by dimension with latency/error metrics.
tier: free
inputs: events, period, group_by
---

# Telemetry Reporter

## Description
Aggregates telemetry events by dimension with latency/error metrics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `events` | `array` | Yes |  |
| `period` | `string` | Yes |  |
| `group_by` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "telemetry_reporter",
  "arguments": {
    "events": [],
    "period": "<period>",
    "group_by": "<group_by>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "telemetry_reporter"`.
