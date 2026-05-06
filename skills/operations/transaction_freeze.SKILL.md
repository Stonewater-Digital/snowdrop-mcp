---
skill: transaction_freeze
category: operations
description: Activates the global freeze flag so downstream payment skills stop immediately.
tier: free
inputs: reason, triggered_by
---

# Transaction Freeze

## Description
Activates the global freeze flag so downstream payment skills stop immediately.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `reason` | `string` | Yes | Short reason for the freeze. |
| `triggered_by` | `string` | Yes | Name or system that pulled the kill-switch. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "transaction_freeze",
  "arguments": {
    "reason": "<reason>",
    "triggered_by": "<triggered_by>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "transaction_freeze"`.
