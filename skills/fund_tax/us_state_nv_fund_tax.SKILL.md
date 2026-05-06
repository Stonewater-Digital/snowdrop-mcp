---
skill: us_state_nv_fund_tax
category: fund_tax
description: Calculates Nevada Commerce Tax exposure for investment funds meeting the $4M receipts trigger. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Nv Fund Tax

## Description
Calculates Nevada Commerce Tax exposure for investment funds meeting the $4M receipts trigger. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_nv_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_nv_fund_tax"`.
