---
skill: compliance_calendar
category: compliance_reporting
description: Generates a consolidated compliance deadline calendar with statuses.
tier: free
inputs: entity, filings, current_date
---

# Compliance Calendar

## Description
Generates a consolidated compliance deadline calendar with statuses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `entity` | `object` | Yes |  |
| `filings` | `array` | Yes |  |
| `current_date` | `string` | Yes | ISO date used as the reference point. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "compliance_calendar",
  "arguments": {
    "entity": {},
    "filings": [],
    "current_date": "<current_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compliance_calendar"`.
