---
skill: co_investment_ledger
category: fund_accounting
description: Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal. Calculates total combined exposure per deal, percentage ownership split, and aggregate exposure totals across the portfolio.
tier: premium
inputs: none
---

# Co Investment Ledger

## Description
Constructs a co-investment ledger for a private equity fund, showing main fund capital alongside co-investor capital for each deal. Calculates total combined exposure per deal, percentage ownership split, and aggregate exposure totals across the portfolio. (Premium — subscribe at https://snowdrop.ai)

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "co_investment_ledger",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "co_investment_ledger"`.
