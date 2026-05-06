---
skill: mlp_growth_capex_return_calculator
category: mlps
description: Evaluates projected EBITDA gains versus growth capex to estimate cash-on-cash returns. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Growth Capex Return Calculator

## Description
Evaluates projected EBITDA gains versus growth capex to estimate cash-on-cash returns. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_growth_capex_return_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_growth_capex_return_calculator"`.
