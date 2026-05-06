---
skill: variance_swap_pricer
category: derivatives
description: Computes fair variance strike, variance notional, and P&L for variance swaps. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Variance Swap Pricer

## Description
Computes fair variance strike, variance notional, and P&L for variance swaps. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "variance_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "variance_swap_pricer"`.
