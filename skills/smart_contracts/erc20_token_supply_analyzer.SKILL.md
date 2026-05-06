---
skill: erc20_token_supply_analyzer
category: smart_contracts
description: Breaks total supply into circulating, treasury, and locked components to monitor float.
tier: free
inputs: total_supply, treasury_tokens, burned_tokens, locked_tokens
---

# Erc20 Token Supply Analyzer

## Description
Breaks total supply into circulating, treasury, and locked components to monitor float.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_supply` | `number` | Yes | Fully diluted token supply |
| `treasury_tokens` | `number` | Yes | Tokens held by treasury wallets |
| `burned_tokens` | `number` | Yes | Tokens sent to burn addresses |
| `locked_tokens` | `number` | Yes | Tokens locked in vesting or contracts |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "erc20_token_supply_analyzer",
  "arguments": {
    "total_supply": 0,
    "treasury_tokens": 0,
    "burned_tokens": 0,
    "locked_tokens": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "erc20_token_supply_analyzer"`.
