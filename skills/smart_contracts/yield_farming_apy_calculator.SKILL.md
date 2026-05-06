---
skill: yield_farming_apy_calculator
category: smart_contracts
description: Translates per-block reward rates into APR and APY estimates for yield farmers.
tier: free
inputs: reward_rate_per_block, blocks_per_day, reward_token_price_usd, staked_value_usd
---

# Yield Farming Apy Calculator

## Description
Translates per-block reward rates into APR and APY estimates for yield farmers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `reward_rate_per_block` | `number` | Yes | Tokens paid per block |
| `blocks_per_day` | `number` | Yes | Expected blocks per day |
| `reward_token_price_usd` | `number` | Yes | USD price of reward token |
| `staked_value_usd` | `number` | Yes | USD value of stake |
| `compound_frequency_days` | `number` | No | Days between reinvestment cycles |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "yield_farming_apy_calculator",
  "arguments": {
    "reward_rate_per_block": 0,
    "blocks_per_day": 0,
    "reward_token_price_usd": 0,
    "staked_value_usd": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "yield_farming_apy_calculator"`.
