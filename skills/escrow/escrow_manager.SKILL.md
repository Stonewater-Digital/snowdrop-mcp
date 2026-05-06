---
skill: escrow_manager
category: escrow
description: Creates, monitors, and adjudicates agent escrow records.
tier: free
inputs: operation, escrow
---

# Escrow Manager

## Description
Creates, monitors, and adjudicates agent escrow records.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes |  |
| `escrow` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "escrow_manager",
  "arguments": {
    "operation": "<operation>",
    "escrow": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "escrow_manager"`.
