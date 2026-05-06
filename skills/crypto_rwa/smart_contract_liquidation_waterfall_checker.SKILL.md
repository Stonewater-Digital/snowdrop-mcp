---
skill: smart_contract_liquidation_waterfall_checker
category: crypto_rwa
description: Validates liquidation waterfalls respect seniority rules across tranches.
tier: free
inputs: none
---

# Smart Contract Liquidation Waterfall Checker

## Description
Validates liquidation waterfalls respect seniority rules across tranches.

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
  "tool": "smart_contract_liquidation_waterfall_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_liquidation_waterfall_checker"`.
