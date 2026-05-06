---
skill: callable_bond_pricer
category: fixed_income_analytics
description: Values a callable bond on a single-factor Hull-White lattice, providing model price, duration, and call exercise probabilities. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Callable Bond Pricer

## Description
Values a callable bond on a single-factor Hull-White lattice, providing model price, duration, and call exercise probabilities. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "callable_bond_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "callable_bond_pricer"`.
