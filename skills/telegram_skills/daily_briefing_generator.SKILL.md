---
skill: daily_briefing_generator
category: telegram_skills
description: Assembles Snowdrop's morning status brief for Thunder.
tier: free
inputs: financials
---

# Daily Briefing Generator

## Description
Assembles Snowdrop's morning status brief for Thunder.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `financials` | `object` | Yes |  |
| `headlines` | `array` | No |  |
| `date_override` | `string` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "daily_briefing_generator",
  "arguments": {
    "financials": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "daily_briefing_generator"`.
