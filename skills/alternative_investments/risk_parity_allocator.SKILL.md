---
skill: risk_parity_allocator
category: alternative_investments
description: Uses iterative proportional fitting on the covariance matrix to achieve target risk budgets per asset. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Risk Parity Allocator

## Description
Uses iterative proportional fitting on the covariance matrix to achieve target risk budgets per asset. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "risk_parity_allocator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_parity_allocator"`.
