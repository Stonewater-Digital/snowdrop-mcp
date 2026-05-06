---
skill: co_investment_ledger
category: fund_accounting
description: Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal. Calculates total combined exposure per deal, percentage ownership split, and aggregate exposure totals across the portfolio.
tier: premium
inputs: deals, fund_name
---

# Co Investment Ledger

## Description
Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal. Calculates total combined exposure per deal, percentage ownership split, and aggregate exposure totals across the portfolio. Premium skill — subscribe at https://snowdrop.ai.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `deals` | `array` | Yes | List of deal objects, each with `deal_name`, `fund_capital` (main fund investment), and `co_investors` (list of co-investor objects with `name` and `capital`). |
| `fund_name` | `string` | No | Display name for the main fund (used in report headers). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "co_investment_ledger",
  "arguments": {
    "deals": [
      {
        "deal_name": "Acme Corp Series B",
        "fund_capital": 10000000,
        "co_investors": [
          {"name": "LP Co-Invest SPV I", "capital": 3000000},
          {"name": "Family Office X", "capital": 2000000}
        ]
      }
    ],
    "fund_name": "Snowdrop PE Fund III"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "co_investment_ledger"`.
