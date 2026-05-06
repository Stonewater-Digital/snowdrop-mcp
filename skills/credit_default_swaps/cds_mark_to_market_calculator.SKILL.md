---
skill: cds_mark_to_market_calculator
category: credit_default_swaps
description: Marks CDS positions using PV01 and spread differentials.
tier: free
inputs: notional, contract_spread_bps, market_spread_bps, discount_factors
---

# Cds Mark To Market Calculator

## Description
Marks CDS positions using PV01 and spread differentials.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `notional` | `number` | Yes |  |
| `contract_spread_bps` | `number` | Yes |  |
| `market_spread_bps` | `number` | Yes |  |
| `discount_factors` | `array` | Yes |  |
| `payment_interval_years` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "cds_mark_to_market_calculator",
  "arguments": {
    "notional": 0,
    "contract_spread_bps": 0,
    "market_spread_bps": 0,
    "discount_factors": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_mark_to_market_calculator"`.
