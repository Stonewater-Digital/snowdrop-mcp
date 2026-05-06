---
skill: commodity_swap_pricer
category: derivatives
description: Prices fixed-for-floating commodity swaps using forward curves and discount factors. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Commodity Swap Pricer

## Description
Prices fixed-for-floating commodity swaps using forward curves and discount factors. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "commodity_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commodity_swap_pricer"`.
