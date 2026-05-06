---
skill: timezone_scheduler
category: i18n
description: Converts event timestamps into relevant time zones and flags off-hour meetings.
tier: free
inputs: events
---

# Timezone Scheduler

## Description
Converts event timestamps into relevant time zones and flags off-hour meetings.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `events` | `array` | Yes |  |
| `display_timezone` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "timezone_scheduler",
  "arguments": {
    "events": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "timezone_scheduler"`.
