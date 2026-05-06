---
skill: rwa_oracle_muni_bond_price_sync
category: crypto_rwa
description: Aligns municipal bond marks from EMMA with on-chain oracle quotes and flags spreads beyond tolerance.
tier: free
inputs: none
---

# Rwa Oracle Muni Bond Price Sync

## Description
Aligns municipal bond marks from EMMA with on-chain oracle quotes and flags spreads beyond tolerance.

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
  "tool": "rwa_oracle_muni_bond_price_sync",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_muni_bond_price_sync"`.
