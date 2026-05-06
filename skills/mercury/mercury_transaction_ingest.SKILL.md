---
skill: mercury_transaction_ingest
category: mercury
description: Pulls Mercury transactions, tags inflow/outflow, and formats for Ghost Ledger.
tier: free
inputs: start_date, end_date
---

# Mercury Transaction Ingest

## Description
Pulls Mercury transactions, tags inflow/outflow, and formats for Ghost Ledger.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `start_date` | `string` | Yes |  |
| `end_date` | `string` | Yes |  |
| `limit` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mercury_transaction_ingest",
  "arguments": {
    "start_date": "<start_date>",
    "end_date": "<end_date>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mercury_transaction_ingest"`.
