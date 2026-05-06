---
skill: prep_daily_intel
category: google_chat
description: Aggregate 24h logs and system health into 3-5 BLUF bullet points for CTO briefing.
tier: free
inputs: none
---

# Prep Daily Intel

## Description
Aggregate 24h logs and system health into 3-5 BLUF bullet points for CTO briefing.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `hours_lookback` | `integer` | No | Hours to look back in logs (default: 24) |
| `include_system_health` | `boolean` | No | Include system health metrics (default: true) |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "prep_daily_intel",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "prep_daily_intel"`.
