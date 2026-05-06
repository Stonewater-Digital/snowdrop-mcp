---
skill: token_standard_solvency_ratio_checker
category: crypto_rwa
description: Checks issuer solvency ratios versus promised buffers before new issuance.
tier: free
inputs: none
---

# Token Standard Solvency Ratio Checker

## Description
Checks issuer solvency ratios versus promised buffers before new issuance.

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
  "tool": "token_standard_solvency_ratio_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_standard_solvency_ratio_checker"`.
