---
skill: agent_heartbeat_monitor
category: technical
description: Build health check monitoring configurations for Fly.io and Railway services. Defines check intervals, alert rules (3 consecutive failures = alert), and per-service configs.
tier: free
inputs: services
---

# Agent Heartbeat Monitor

## Description
Build health check monitoring configurations for Fly.io and Railway services. Defines check intervals, alert rules (3 consecutive failures = alert), and per-service configs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `services` | `array` | Yes | List of service dicts, each with: name, url, expected_status (HTTP status code), timeout_seconds. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_heartbeat_monitor",
  "arguments": {
    "services": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_heartbeat_monitor"`.
