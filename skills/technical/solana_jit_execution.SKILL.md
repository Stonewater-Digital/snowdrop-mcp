---
skill: solana_jit_execution
category: technical
description: Calculate Just-in-Time liquidity provisioning plan for a Solana AMM pool with yield estimation and risk scoring.
tier: free
inputs: pool_address, token_pair, amount_usd, slippage_tolerance_bps
---

# Solana Jit Execution

## Description
Calculate Just-in-Time liquidity provisioning plan for a Solana AMM pool with yield estimation and risk scoring.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pool_address` | `string` | Yes | The Solana AMM pool public key address. |
| `token_pair` | `string` | Yes | Token pair string, e.g. 'SOL/USDC'. |
| `amount_usd` | `number` | Yes | USD value of the JIT liquidity position to provide. |
| `slippage_tolerance_bps` | `integer` | Yes | Maximum acceptable slippage in basis points (e.g. 50 = 0.5%). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "solana_jit_execution",
  "arguments": {
    "pool_address": "<pool_address>",
    "token_pair": "<token_pair>",
    "amount_usd": 0,
    "slippage_tolerance_bps": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "solana_jit_execution"`.
