---
skill: ghost_ledger_reconciler
category: ghost_ledger
description: Compare ledger snapshots to live balances with zero-tolerance policy.
tier: free
inputs: ledger_balances, live_balances
---

# Ghost Ledger Reconciler

## Description
Compare ledger snapshots to live balances with zero-tolerance policy.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `ledger_balances` | `object` | Yes |  |
| `live_balances` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ghost_ledger_reconciler",
  "arguments": {
    "ledger_balances": {},
    "live_balances": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ghost_ledger_reconciler"`.
