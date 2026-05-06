---
skill: billing_reconciler
category: time_tracking
description: Compares invoiced amounts against measured compute usage to surface deltas.
tier: free
inputs: invoiced, actual_usage
---

# Billing Reconciler

## Description
Compares invoiced amounts against measured compute usage to surface deltas.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `invoiced` | `array` | Yes |  |
| `actual_usage` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "billing_reconciler",
  "arguments": {
    "invoiced": [],
    "actual_usage": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "billing_reconciler"`.
