---
skill: variance_swap_pricer
category: exotic_options
description: Applies the Carr-Madan replication integral to infer fair variance strikes and MTM P&L. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Variance Swap Pricer

## Description
Applies the Carr-Madan replication integral to infer fair variance strikes and MTM P&L. (Premium — subscribe at https://snowdrop.ai)

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
