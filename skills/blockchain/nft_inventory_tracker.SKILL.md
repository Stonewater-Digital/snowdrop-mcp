---
skill: nft_inventory_tracker
category: blockchain
description: Aggregates NFT holdings with valuation deltas and allocation mix.
tier: free
inputs: wallets, known_nfts
---

# Nft Inventory Tracker

## Description
Aggregates NFT holdings with valuation deltas and allocation mix.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `wallets` | `array` | Yes |  |
| `known_nfts` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nft_inventory_tracker",
  "arguments": {
    "wallets": [],
    "known_nfts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nft_inventory_tracker"`.
