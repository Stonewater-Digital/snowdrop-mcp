---
skill: correlation_swap_pricer
category: structured_products
description: Computes the fair correlation (average off-diagonal) and marks the swap relative to strike with delta/vega style metrics. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Correlation Swap Pricer

## Description
Computes the fair correlation (average off-diagonal) and marks the swap relative to strike with delta/vega style metrics. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "correlation_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "correlation_swap_pricer"`.
