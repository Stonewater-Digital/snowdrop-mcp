---
skill: system_health_composite
category: health
description: Rolls subsystem telemetry into a weighted score and recommendations.
tier: free
inputs: subsystems
---

# System Health Composite

## Description
Rolls subsystem telemetry into a weighted score and recommendations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `subsystems` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "system_health_composite",
  "arguments": {
    "subsystems": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "system_health_composite"`.
