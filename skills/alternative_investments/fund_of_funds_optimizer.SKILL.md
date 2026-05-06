---
skill: fund_of_funds_optimizer
category: alternative_investments
description: Uses scenario analysis with CVaR targeting to produce FoF weights under allocation caps. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Fund Of Funds Optimizer

## Description
Uses scenario analysis with CVaR targeting to produce FoF weights under allocation caps. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "fund_of_funds_optimizer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_of_funds_optimizer"`.
