---
skill: performance_poller_control
category: social
description: Observe, trigger, or read the status of the Snowdrop Performance Poller subagent (A2A protocol). Actions: 'status' (last run time, posts polled, errors), 'trigger' (run poller immediately via subprocess), 'read_card' (return the A2A agent card JSON), 'read_log' (last N lines of poller log).
tier: free
inputs: none
---

# Performance Poller Control

## Description
Observe, trigger, or read the status of the Snowdrop Performance Poller subagent (A2A protocol). Actions: 'status' (last run time, posts polled, errors), 'trigger' (run poller immediately via subprocess), 'read_card' (return the A2A agent card JSON), 'read_log' (last N lines of poller log). The poller normally runs every 2h via cron but can be triggered on-demand.

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
  "tool": "performance_poller_control",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "performance_poller_control"`.
