---
skill: agent_heartbeat_collector
category: swarm
description: Rolls up heartbeat telemetry and surfaces degraded/dead agents.
tier: free
inputs: heartbeats
---

# Agent Heartbeat Collector

## Description
Rolls up heartbeat telemetry and surfaces degraded/dead agents.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `heartbeats` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "agent_heartbeat_collector",
  "arguments": {
    "heartbeats": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "agent_heartbeat_collector"`.
