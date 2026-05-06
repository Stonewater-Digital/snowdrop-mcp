---
skill: rwa_token_valuation_model
category: rwa_tokenization
description: Discounts projected cash flows to derive intrinsic value per RWA token.
tier: free
inputs: cash_flows, discount_rate_pct, token_supply
---

# Rwa Token Valuation Model

## Description
Discounts projected cash flows to derive intrinsic value per RWA token.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `cash_flows` | `array` | Yes | Projected cash flows with timing in years. |
| `discount_rate_pct` | `number` | Yes | Annual discount rate |
| `token_supply` | `number` | Yes | Outstanding token count |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_token_valuation_model",
  "arguments": {
    "cash_flows": [],
    "discount_rate_pct": 0,
    "token_supply": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_token_valuation_model"`.
