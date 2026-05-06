---
skill: staking_yield_calculator
category: smart_contracts
description: Analyzes staking rewards to derive APR, payout cadence, and token emissions.
tier: free
inputs: total_staked_tokens, annual_inflation_tokens
---

# Staking Yield Calculator

## Description
Analyzes staking rewards to derive APR, payout cadence, and token emissions.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_staked_tokens` | `number` | Yes | Total tokens staked in the network |
| `annual_inflation_tokens` | `number` | Yes | Tokens emitted to stakers annually |
| `commission_pct` | `number` | No | Validator/delegation commission percent |
| `token_price_usd` | `number` | No | Token USD price |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "staking_yield_calculator",
  "arguments": {
    "total_staked_tokens": 0,
    "annual_inflation_tokens": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "staking_yield_calculator"`.
