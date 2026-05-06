---
skill: bond_relative_value
category: fixed_income_analytics
description: Calculates Z-spread via discount-factor root search, approximates asset swap spread versus swaps, and derives CDS basis. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Bond Relative Value

## Description
Calculates Z-spread via discount-factor root search, approximates asset swap spread versus swaps, and derives CDS basis. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "bond_relative_value",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_relative_value"`.
