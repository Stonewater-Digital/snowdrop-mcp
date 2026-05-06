---
skill: api_health_monitor
category: technical
description: Performs lightweight health checks and scores availability.
tier: free
inputs: endpoints
---

# Api Health Monitor

## Description
Performs lightweight health checks and scores availability.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `endpoints` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "api_health_monitor",
  "arguments": {
    "endpoints": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "api_health_monitor"`.
