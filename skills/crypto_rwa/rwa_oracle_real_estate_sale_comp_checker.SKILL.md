---
skill: rwa_oracle_real_estate_sale_comp_checker
category: crypto_rwa
description: Confirms sale comparables feeding residential tokens align with MLS data.
tier: free
inputs: none
---

# Rwa Oracle Real Estate Sale Comp Checker

## Description
Confirms sale comparables feeding residential tokens align with MLS data.

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
  "tool": "rwa_oracle_real_estate_sale_comp_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_oracle_real_estate_sale_comp_checker"`.
