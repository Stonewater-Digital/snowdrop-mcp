---
skill: tokenized_commodity_basis_tracker
category: rwa_tokenization
description: Compares token prices against spot commodity benchmarks adjusting for carry costs.
tier: free
inputs: spot_price, token_price
---

# Tokenized Commodity Basis Tracker

## Description
Compares token prices against spot commodity benchmarks adjusting for carry costs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `spot_price` | `number` | Yes | Benchmark spot price |
| `token_price` | `number` | Yes | Market price of the commodity token |
| `storage_cost_pct` | `number` | No | Annual storage/carry cost percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tokenized_commodity_basis_tracker",
  "arguments": {
    "spot_price": 0,
    "token_price": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tokenized_commodity_basis_tracker"`.
