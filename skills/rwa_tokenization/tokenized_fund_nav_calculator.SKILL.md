---
skill: tokenized_fund_nav_calculator
category: rwa_tokenization
description: Aggregates asset values minus liabilities to derive NAV per RWA token.
tier: free
inputs: asset_values, liabilities, token_supply
---

# Tokenized Fund Nav Calculator

## Description
Aggregates asset values minus liabilities to derive NAV per RWA token.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `asset_values` | `array` | Yes | List of asset fair values |
| `liabilities` | `number` | Yes | Total liabilities |
| `token_supply` | `number` | Yes | Token units outstanding |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tokenized_fund_nav_calculator",
  "arguments": {
    "asset_values": [],
    "liabilities": 0,
    "token_supply": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tokenized_fund_nav_calculator"`.
