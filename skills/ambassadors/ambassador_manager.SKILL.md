---
skill: ambassador_manager
category: ambassadors
description: Handles ambassador applications, approvals, listings, and removals.
tier: free
inputs: operation
---

# Ambassador Manager

## Description
Handles ambassador applications, approvals, listings, and removals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `ambassador` | `['object', 'null']` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ambassador_manager",
  "arguments": {
    "operation": "<operation>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ambassador_manager"`.
