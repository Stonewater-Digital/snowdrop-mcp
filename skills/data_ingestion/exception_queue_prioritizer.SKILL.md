---
skill: exception_queue_prioritizer
category: data_ingestion
description: Prioritize reconciliation exceptions by severity, financial exposure, and SLA breach risk.
tier: free
inputs: exceptions
---

# Exception Queue Prioritizer

## Description
Prioritize reconciliation exceptions by severity, financial exposure, and SLA breach risk.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exceptions` | `array` | Yes | Exception payloads with fields: id, severity, detected_at, type, attempts, amount_at_risk. |
| `owner_map` | `object` | No | Keyword -> owner/team overrides for routing. |
| `max_items` | `integer` | No | Maximum prioritized exceptions to return. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "exception_queue_prioritizer",
  "arguments": {
    "exceptions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "exception_queue_prioritizer"`.
