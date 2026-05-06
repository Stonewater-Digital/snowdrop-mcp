---
skill: rwa_custody_cost_calculator
category: rwa_tokenization
description: Summarizes custody expenses for RWA structures using AUC fees and retainers.
tier: free
inputs: assets_under_custody, custody_fee_bps, flat_fee_usd
---

# Rwa Custody Cost Calculator

## Description
Summarizes custody expenses for RWA structures using AUC fees and retainers.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `assets_under_custody` | `number` | Yes | Collateral value held by custodian |
| `custody_fee_bps` | `number` | Yes | Annual basis points on AUC |
| `flat_fee_usd` | `number` | Yes | Annual retainer |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_custody_cost_calculator",
  "arguments": {
    "assets_under_custody": 0,
    "custody_fee_bps": 0,
    "flat_fee_usd": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_custody_cost_calculator"`.
