---
skill: request_queue_manager
category: gateway
description: Manages enqueue/dequeue/peek/stats for agent request queues.
tier: free
inputs: operation, queue_state
---

# Request Queue Manager

## Description
Manages enqueue/dequeue/peek/stats for agent request queues.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `request` | `['object', 'null']` | No |  |
| `queue_state` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "request_queue_manager",
  "arguments": {
    "operation": "<operation>",
    "queue_state": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "request_queue_manager"`.
