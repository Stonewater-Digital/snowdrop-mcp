---
skill: position_reconciliation_tool
category: middle_office
description: Compares internal books with prime broker files and flags breaks.
tier: free
inputs: internal_positions, broker_positions
---

# Position Reconciliation Tool

## Description
Compares internal books with prime broker files and flags breaks.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `internal_positions` | `array` | Yes |  |
| `broker_positions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "position_reconciliation_tool",
  "arguments": {
    "internal_positions": [],
    "broker_positions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "position_reconciliation_tool"`.
