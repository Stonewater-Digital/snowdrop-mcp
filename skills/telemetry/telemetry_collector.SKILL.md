---
skill: telemetry_collector
category: telemetry
description: Appends anonymous usage telemetry after stripping PII.
tier: free
inputs: event_type, properties
---

# Telemetry Collector

## Description
Appends anonymous usage telemetry after stripping PII.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `event_type` | `string` | Yes |  |
| `properties` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "telemetry_collector",
  "arguments": {
    "event_type": "<event_type>",
    "properties": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "telemetry_collector"`.
