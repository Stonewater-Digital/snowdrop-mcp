---
skill: gp_co_invest_calculator
category: fund_admin
description: Calculates GP and LP capital allocations plus promote economics for co-investment deals. Returns GP commitment, LP commitment, and the promote pool available for the GP.
tier: premium
inputs: none
---

# Gp Co Invest Calculator

## Description
Calculates GP and LP capital allocations plus promote economics for co-investment deals. Returns GP commitment, LP commitment, and the promote pool available for the GP. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "gp_co_invest_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gp_co_invest_calculator"`.
