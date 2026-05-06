---
skill: co_investment_analyzer
category: alternative_investments
description: Calculates fee savings, carry relief, and net IRR uplift from co-investment structures. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Co Investment Analyzer

## Description
Calculates fee savings, carry relief, and net IRR uplift from co-investment structures. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "co_investment_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "co_investment_analyzer"`.
