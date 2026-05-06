---
skill: rwa_oracle_t_bill_fx_cross_checker
category: crypto_rwa
description: Ensures T-bill tokens priced in non-USD denominations reflect live FX crosses.
tier: free
inputs: none
---

# Rwa Oracle T Bill Fx Cross Checker

## Description
Ensures T-bill tokens priced in non-USD denominations reflect live FX crosses.

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
  "tool": "rwa_oracle_t_bill_fx_cross_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_t_bill_fx_cross_checker"`.
