---
skill: transaction_ingest_bridge
category: fund_accounting
description: Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: mercury_feed, kraken_feed
---

# Transaction Ingest Bridge

## Description
Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion. (Premium — subscribe at https://snowdrop.ai)

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `mercury_feed` | `array` | No | List of Mercury bank transaction objects to normalize and ingest. At least one of `mercury_feed` or `kraken_feed` must be provided. |
| `kraken_feed` | `array` | No | List of Kraken exchange transaction objects to normalize and ingest. At least one of `mercury_feed` or `kraken_feed` must be provided. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "transaction_ingest_bridge",
  "arguments": {
    "mercury_feed": [
      {"id": "merc_abc123", "date": "2026-05-01", "amount": -15000.00, "description": "Wire to Portfolio Co Alpha", "counterparty": "Alpha Inc", "type": "outgoing_wire"},
      {"id": "merc_abc124", "date": "2026-05-03", "amount": 250000.00, "description": "LP capital call receipt", "counterparty": "State Pension Fund", "type": "incoming_wire"}
    ],
    "kraken_feed": null
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "transaction_ingest_bridge"`.
