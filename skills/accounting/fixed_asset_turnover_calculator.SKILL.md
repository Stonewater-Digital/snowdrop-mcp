---
skill: fixed_asset_turnover_calculator
category: accounting
description: Calculates the fixed asset turnover ratio, measuring how efficiently a company generates revenue from its net fixed assets (PP&E).
tier: free
inputs: net_sales, net_fixed_assets
---

# Fixed Asset Turnover Calculator

## Description
Calculates the fixed asset turnover ratio, measuring how efficiently a company generates revenue from its net fixed assets (PP&E).

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `net_sales` | `number` | Yes | Net sales (revenue) for the period. |
| `net_fixed_assets` | `number` | Yes | Net fixed assets (property, plant & equipment less depreciation). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fixed_asset_turnover_calculator",
  "arguments": {
    "net_sales": 0,
    "net_fixed_assets": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fixed_asset_turnover_calculator"`.
