---
skill: mvrv_ratio_calculator
category: blockchain_analytics
description: Computes Market Value to Realized Value ratio to identify accumulation or euphoria regimes.
tier: free
inputs: market_cap, realized_cap
---

# Mvrv Ratio Calculator

## Description
Computes Market Value to Realized Value ratio to identify accumulation or euphoria regimes.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `market_cap` | `number` | Yes | Spot market capitalization for the asset in USD. |
| `realized_cap` | `number` | Yes | Realized capitalization derived from UTXO or cost-basis ledgers in USD. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "mvrv_ratio_calculator",
  "arguments": {
    "market_cap": 0,
    "realized_cap": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mvrv_ratio_calculator"`.
