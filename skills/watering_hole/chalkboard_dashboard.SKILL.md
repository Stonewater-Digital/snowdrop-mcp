---
skill: chalkboard_dashboard
category: watering_hole
description: Aggregates transparency metrics for the public chalkboard dashboard.
tier: free
inputs: financials, agent_stats
---

# Chalkboard Dashboard

## Description
Aggregates transparency metrics for the public chalkboard dashboard.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `financials` | `object` | Yes | Key P&L figures for the period. |
| `agent_stats` | `array` | Yes | Agent contribution telemetry. |
| `notable_events` | `array` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "chalkboard_dashboard",
  "arguments": {
    "financials": {},
    "agent_stats": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chalkboard_dashboard"`.
