---
skill: nft_royalty_cashflow_calculator
category: smart_contracts
description: Calculates gross and net royalty cash flows using volume, pricing, and fee inputs.
tier: free
inputs: royalty_rate_pct, average_sale_price, monthly_sales
---

# Nft Royalty Cashflow Calculator

## Description
Calculates gross and net royalty cash flows using volume, pricing, and fee inputs.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `royalty_rate_pct` | `number` | Yes | Royalty percent applied on each sale |
| `average_sale_price` | `number` | Yes | Average NFT sale price |
| `monthly_sales` | `number` | Yes | Number of secondary sales per month |
| `platform_fee_pct` | `number` | No | Marketplace fee percent |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nft_royalty_cashflow_calculator",
  "arguments": {
    "royalty_rate_pct": 0,
    "average_sale_price": 0,
    "monthly_sales": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nft_royalty_cashflow_calculator"`.
