---
skill: asset_turnover_calculator
category: accounting
description: Calculates the asset turnover ratio, measuring how efficiently a company generates revenue from its total assets.
tier: free
inputs: net_sales, avg_total_assets
---

# Asset Turnover Calculator

## Description
Calculates the asset turnover ratio, measuring how efficiently a company generates revenue from its total assets.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_sales` | `number` | Yes | Net sales (revenue) for the period. |
| `avg_total_assets` | `number` | Yes | Average total assets for the period. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "asset_turnover_calculator",
  "arguments": {
    "net_sales": 0,
    "avg_total_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asset_turnover_calculator"`.
