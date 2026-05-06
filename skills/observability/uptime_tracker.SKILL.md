---
skill: uptime_tracker
category: observability
description: Calculates uptime %, MTBF, MTTR, and outage extremes from heartbeat logs.
tier: free
inputs: heartbeat_log
---

# Uptime Tracker

## Description
Calculates uptime %, MTBF, MTTR, and outage extremes from heartbeat logs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `heartbeat_log` | `array` | Yes |  |
| `period_hours` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "uptime_tracker",
  "arguments": {
    "heartbeat_log": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "uptime_tracker"`.
