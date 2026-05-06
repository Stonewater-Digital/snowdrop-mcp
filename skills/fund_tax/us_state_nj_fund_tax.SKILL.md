---
skill: us_state_nj_fund_tax
category: fund_tax
description: Computes New Jersey individual tax proxies, BAIT election effect, and nonresident withholding for LP interests. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Nj Fund Tax

## Description
Computes New Jersey individual tax proxies, BAIT election effect, and nonresident withholding for LP interests. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_nj_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_nj_fund_tax"`.
