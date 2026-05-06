---
skill: prime_broker_reconciliation
category: middle_office
description: Reconciles positions and cash between internal books and the prime broker.
tier: free
inputs: internal_positions, pb_positions, internal_cash, pb_cash
---

# Prime Broker Reconciliation

## Description
Reconciles positions and cash between internal books and the prime broker.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `internal_positions` | `array` | Yes |  |
| `pb_positions` | `array` | Yes |  |
| `internal_cash` | `number` | Yes |  |
| `pb_cash` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "prime_broker_reconciliation",
  "arguments": {
    "internal_positions": [],
    "pb_positions": [],
    "internal_cash": 0,
    "pb_cash": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "prime_broker_reconciliation"`.
