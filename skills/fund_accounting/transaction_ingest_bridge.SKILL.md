---
skill: transaction_ingest_bridge
category: fund_accounting
description: Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Transaction Ingest Bridge

## Description
Fetches or accepts Mercury/Kraken transaction payloads and normalizes them for Ghost Ledger ingestion. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "transaction_ingest_bridge",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "transaction_ingest_bridge"`.
