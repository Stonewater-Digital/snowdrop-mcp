---
skill: fund_leverage_analyzer
category: fund_admin
description: Calculates fund-level leverage ratios including subscription line leverage, asset-level debt, look-through leverage, and debt-to-equity ratios. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Fund Leverage Analyzer

## Description
Calculates fund-level leverage ratios including subscription line leverage, asset-level debt, look-through leverage, and debt-to-equity ratios. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "fund_leverage_analyzer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fund_leverage_analyzer"`.
