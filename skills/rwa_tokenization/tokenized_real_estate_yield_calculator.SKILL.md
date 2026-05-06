---
skill: tokenized_real_estate_yield_calculator
category: rwa_tokenization
description: Computes NOI yield for tokenized real estate including leverage cost adjustments.
tier: free
inputs: gross_rent, operating_expenses, token_market_value
---

# Tokenized Real Estate Yield Calculator

## Description
Computes NOI yield for tokenized real estate including leverage cost adjustments.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `gross_rent` | `number` | Yes | Annualized rental income |
| `operating_expenses` | `number` | Yes | Annual operating expenses |
| `interest_expense` | `number` | No | Annual debt service |
| `token_market_value` | `number` | Yes | Current market cap of tokens |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "tokenized_real_estate_yield_calculator",
  "arguments": {
    "gross_rent": 0,
    "operating_expenses": 0,
    "token_market_value": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tokenized_real_estate_yield_calculator"`.
