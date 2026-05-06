---
skill: credit_spread_decomposer
category: fixed_income_analytics
description: Breaks a corporate bond option-adjusted spread into expected loss (PD*LGD), liquidity premium, risk premium, and tax component per BIS credit risk methodology. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Credit Spread Decomposer

## Description
Breaks a corporate bond option-adjusted spread into expected loss (PD*LGD), liquidity premium, risk premium, and tax component per BIS credit risk methodology. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "credit_spread_decomposer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_spread_decomposer"`.
