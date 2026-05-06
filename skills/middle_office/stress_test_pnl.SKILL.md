---
skill: stress_test_pnl
category: middle_office
description: Applies factor shocks to estimate stressed P&L for positions.
tier: free
inputs: positions, shocks
---

# Stress Test Pnl

## Description
Applies factor shocks to estimate stressed P&L for positions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `positions` | `array` | Yes |  |
| `shocks` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "stress_test_pnl",
  "arguments": {
    "positions": [],
    "shocks": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stress_test_pnl"`.
