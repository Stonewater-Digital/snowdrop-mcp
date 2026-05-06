---
skill: waterfall_sensitivity_analyzer
category: fund_admin
description: Evaluates GP carry payouts across a grid of hurdle rates and carry percentages using a full 4-tier waterfall (ROC, pref, catch-up, split). Returns a sensitivity matrix and identifies optimal scenarios.
tier: premium
inputs: none
---

# Waterfall Sensitivity Analyzer

## Description
Evaluates GP carry payouts across a grid of hurdle rates and carry percentages using a full 4-tier waterfall (ROC, pref, catch-up, split). Returns a sensitivity matrix and identifies optimal scenarios. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "waterfall_sensitivity_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "waterfall_sensitivity_analyzer"`.
