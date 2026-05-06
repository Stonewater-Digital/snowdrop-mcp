---
skill: daemon_health_dashboard
category: system
description: Aggregate health status of all Snowdrop daemons, timers, and cron jobs into a single dashboard view.
tier: free
inputs: none
---

# Daemon Health Dashboard

## Description
Aggregate health status of all Snowdrop daemons, timers, and cron jobs into a single dashboard view.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "daemon_health_dashboard",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "daemon_health_dashboard"`.
