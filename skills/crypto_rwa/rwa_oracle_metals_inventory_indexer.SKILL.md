---
skill: rwa_oracle_metals_inventory_indexer
category: crypto_rwa
description: Reconciles LME inventory data against tokenized warehouse receipt feeds.
tier: free
inputs: payload
---

# Rwa Oracle Metals Inventory Indexer

## Description
Reconciles LME inventory data against tokenized warehouse receipt feeds.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_oracle_metals_inventory_indexer",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_metals_inventory_indexer"`.
