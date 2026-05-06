---
skill: transaction_anomaly_flagger
category: anomaly
description: Scores transactions for amount, counterparty, category, and timing anomalies.
tier: free
inputs: transactions, history_stats
---

# Transaction Anomaly Flagger

## Description
Scores transactions for amount, counterparty, category, and timing anomalies.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transactions` | `array` | Yes |  |
| `history_stats` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "transaction_anomaly_flagger",
  "arguments": {
    "transactions": [],
    "history_stats": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "transaction_anomaly_flagger"`.
