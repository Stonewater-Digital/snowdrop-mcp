---
skill: event_correlator
category: events
description: Evaluates correlation rules to surface compound incidents.
tier: free
inputs: events, correlation_rules
---

# Event Correlator

## Description
Evaluates correlation rules to surface compound incidents.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `events` | `array` | Yes |  |
| `correlation_rules` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "event_correlator",
  "arguments": {
    "events": [],
    "correlation_rules": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "event_correlator"`.
