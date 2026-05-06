---
skill: tail_risk_hedging_cost
category: alternative_investments
description: Aggregates put option strikes/premiums to estimate hedge cost, drawdown coverage, and breakeven levels. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Tail Risk Hedging Cost

## Description
Aggregates put option strikes/premiums to estimate hedge cost, drawdown coverage, and breakeven levels. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "tail_risk_hedging_cost",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "tail_risk_hedging_cost"`.
