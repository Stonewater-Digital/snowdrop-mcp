---
skill: rwa_oracle_collateral_liquidity_flagger
category: crypto_rwa
description: Flags collateral where oracle liquidity inputs diverge from on-chain trades.
tier: free
inputs: none
---

# Rwa Oracle Collateral Liquidity Flagger

## Description
Flags collateral where oracle liquidity inputs diverge from on-chain trades.

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
  "tool": "rwa_oracle_collateral_liquidity_flagger",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_collateral_liquidity_flagger"`.
