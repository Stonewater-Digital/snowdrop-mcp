---
skill: nvt_ratio_calculator
category: blockchain_analytics
description: Computes Willy Woo's Network Value to Transactions ratio with smoothing to classify valuation zones.
tier: free
inputs: market_cap, daily_transaction_volume_usd, smoothing_period
---

# Nvt Ratio Calculator

## Description
Computes Willy Woo's Network Value to Transactions ratio with smoothing to classify valuation zones.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `market_cap` | `number` | Yes | Total network market capitalization in USD. |
| `daily_transaction_volume_usd` | `number` | Yes | Daily on-chain transaction volume settled on the network, denominated in USD. |
| `smoothing_period` | `number` | Yes | Number of days for the exponential smoothing factor (minimum 1). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "nvt_ratio_calculator",
  "arguments": {
    "market_cap": 0,
    "daily_transaction_volume_usd": 0,
    "smoothing_period": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "nvt_ratio_calculator"`.
