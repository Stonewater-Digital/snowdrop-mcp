---
skill: asset_tokenization_fee_estimator
category: rwa_tokenization
description: Aggregates setup and recurring platform fees to forecast tokenization economics.
tier: free
inputs: setup_fee_usd, aum_usd, aum_fee_bps, annual_transaction_volume_usd, transaction_fee_pct
---

# Asset Tokenization Fee Estimator

## Description
Aggregates setup and recurring platform fees to forecast tokenization economics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `setup_fee_usd` | `number` | Yes | One-time onboarding fee |
| `aum_usd` | `number` | Yes | Assets under management |
| `aum_fee_bps` | `number` | Yes | Annual basis points on AUM |
| `annual_transaction_volume_usd` | `number` | Yes | Expected annual transaction volume |
| `transaction_fee_pct` | `number` | Yes | Transaction fee percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "asset_tokenization_fee_estimator",
  "arguments": {
    "setup_fee_usd": 0,
    "aum_usd": 0,
    "aum_fee_bps": 0,
    "annual_transaction_volume_usd": 0,
    "transaction_fee_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_tokenization_fee_estimator"`.
