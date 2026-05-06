---
skill: callable_bond_oas
category: structured_products
description: Builds a Black-Derman-Toy short-rate lattice calibrated to the input curve and solves for the OAS that matches market price, then reports duration and convexity. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Callable Bond Oas

## Description
Builds a Black-Derman-Toy short-rate lattice calibrated to the input curve and solves for the OAS that matches market price, then reports duration and convexity. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "callable_bond_oas",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "callable_bond_oas"`.
