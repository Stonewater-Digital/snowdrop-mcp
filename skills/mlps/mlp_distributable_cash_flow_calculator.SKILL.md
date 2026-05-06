---
skill: mlp_distributable_cash_flow_calculator
category: mlps
description: Derives MLP distributable cash flow from EBITDA, capex, and non-cash adjustments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Distributable Cash Flow Calculator

## Description
Derives MLP distributable cash flow from EBITDA, capex, and non-cash adjustments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_distributable_cash_flow_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_distributable_cash_flow_calculator"`.
