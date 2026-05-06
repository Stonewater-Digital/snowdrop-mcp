---
skill: rwa_oracle_metals_inventory_indexer
category: crypto_rwa
description: Reconciles LME inventory data against tokenized warehouse receipt feeds.
tier: free
inputs: none
---

# Rwa Oracle Metals Inventory Indexer

## Description
Reconciles LME inventory data against tokenized warehouse receipt feeds.

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
  "tool": "rwa_oracle_metals_inventory_indexer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_metals_inventory_indexer"`.
