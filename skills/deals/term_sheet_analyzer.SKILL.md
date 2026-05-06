---
skill: term_sheet_analyzer
category: deals
description: Evaluates post-money, ownership, and liquidation waterfalls for venture deals.
tier: free
inputs: pre_money_valuation, investment_amount, liquidation_preference, participation, anti_dilution, option_pool_pct
---

# Term Sheet Analyzer

## Description
Evaluates post-money, ownership, and liquidation waterfalls for venture deals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `pre_money_valuation` | `number` | Yes |  |
| `investment_amount` | `number` | Yes |  |
| `liquidation_preference` | `number` | Yes |  |
| `participation` | `boolean` | Yes |  |
| `anti_dilution` | `string` | Yes |  |
| `option_pool_pct` | `number` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "term_sheet_analyzer",
  "arguments": {
    "pre_money_valuation": 0,
    "investment_amount": 0,
    "liquidation_preference": 0,
    "participation": false,
    "anti_dilution": "<anti_dilution>",
    "option_pool_pct": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "term_sheet_analyzer"`.
