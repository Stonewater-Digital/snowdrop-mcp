---
skill: mlp_k1_income_allocator
category: mlps
description: Allocates taxable income across unitholders based on ownership units. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Mlp K1 Income Allocator

## Description
Allocates taxable income across unitholders based on ownership units. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "mlp_k1_income_allocator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mlp_k1_income_allocator"`.
