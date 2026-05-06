---
skill: credit_default_swap_pricer
category: derivatives
description: Prices a CDS using flat hazard and discount rates, returning par spread and PVs. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Credit Default Swap Pricer

## Description
Prices a CDS using flat hazard and discount rates, returning par spread and PVs. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "credit_default_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_default_swap_pricer"`.
