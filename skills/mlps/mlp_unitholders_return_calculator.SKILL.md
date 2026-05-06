---
skill: mlp_unitholders_return_calculator
category: mlps
description: Calculates price and distribution contribution to total return for MLP units. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp Unitholders Return Calculator

## Description
Calculates price and distribution contribution to total return for MLP units. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_unitholders_return_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_unitholders_return_calculator"`.
