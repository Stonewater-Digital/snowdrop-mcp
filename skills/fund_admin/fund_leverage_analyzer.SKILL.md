---
skill: fund_leverage_analyzer
category: fund_admin
description: Calculates fund-level leverage ratios including subscription line leverage, asset-level debt, look-through leverage, and debt-to-equity ratios. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: nav, subscription_line_debt, asset_level_debt, gross_asset_value
---

# Fund Leverage Analyzer

## Description
Calculates fund-level leverage ratios including subscription line leverage, asset-level debt, look-through leverage, and debt-to-equity ratios. (Premium — subscribe at https://snowdrop.ai)

## Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| nav | number | Yes | Fund net asset value (LP equity) at the measurement date (USD) |
| subscription_line_debt | number | Yes | Outstanding balance on the fund's subscription credit facility (USD) |
| asset_level_debt | number | Yes | Total portfolio company or asset-level debt held in fund investments (USD) |
| gross_asset_value | number | No | Gross asset value before deducting liabilities; if omitted, computed as nav + total debt |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "fund_leverage_analyzer",
  "arguments": {
    "nav": 75000000,
    "subscription_line_debt": 15000000,
    "asset_level_debt": 40000000,
    "gross_asset_value": 135000000
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_leverage_analyzer"`.
