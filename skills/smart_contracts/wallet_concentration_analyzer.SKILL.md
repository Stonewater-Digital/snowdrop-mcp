---
skill: wallet_concentration_analyzer
category: smart_contracts
description: Analyzes wallet balance data to quantify concentration risk and whale dominance.
tier: free
inputs: wallet_balances
---

# Wallet Concentration Analyzer

## Description
Analyzes wallet balance data to quantify concentration risk and whale dominance.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `wallet_balances` | `array` | Yes | Token balances per wallet |
| `top_n_threshold` | `integer` | No | Number of wallets to aggregate in the top cohort |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "wallet_concentration_analyzer",
  "arguments": {
    "wallet_balances": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "wallet_concentration_analyzer"`.
