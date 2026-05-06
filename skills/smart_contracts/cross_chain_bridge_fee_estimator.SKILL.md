---
skill: cross_chain_bridge_fee_estimator
category: smart_contracts
description: Estimates total bridge fees including relayer markup and destination chain execution gas.
tier: free
inputs: transfer_amount, base_fee, variable_fee_bps
---

# Cross Chain Bridge Fee Estimator

## Description
Estimates total bridge fees including relayer markup and destination chain execution gas.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `transfer_amount` | `number` | Yes | Amount to transfer on source chain |
| `base_fee` | `number` | Yes | Flat protocol fee |
| `variable_fee_bps` | `number` | Yes | Basis point fee on transfer amount |
| `relayer_markup_pct` | `number` | No | Relayer markup percent |
| `dst_gas_units` | `number` | No | Destination chain gas usage |
| `dst_gas_price_native` | `number` | No | Destination chain gas price in native token |
| `native_token_price_usd` | `number` | No | Destination native token USD price |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cross_chain_bridge_fee_estimator",
  "arguments": {
    "transfer_amount": 0,
    "base_fee": 0,
    "variable_fee_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cross_chain_bridge_fee_estimator"`.
