---
skill: smart_contract_gas_estimator
category: smart_contracts
description: Aggregates gas consumption inputs and converts them to native and USD fee estimates.
tier: free
inputs: operations, base_fee_gwei, priority_fee_gwei, native_token_price_usd
---

# Smart Contract Gas Estimator

## Description
Aggregates gas consumption inputs and converts them to native and USD fee estimates.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operations` | `array` | Yes | Sequence of planned contract calls with gas estimates. |
| `base_fee_gwei` | `number` | Yes | Projected base fee per gas in gwei |
| `priority_fee_gwei` | `number` | Yes | Priority tip per gas in gwei |
| `native_token_price_usd` | `number` | Yes | Spot price of the native token in USD |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "smart_contract_gas_estimator",
  "arguments": {
    "operations": [],
    "base_fee_gwei": 0,
    "priority_fee_gwei": 0,
    "native_token_price_usd": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_gas_estimator"`.
