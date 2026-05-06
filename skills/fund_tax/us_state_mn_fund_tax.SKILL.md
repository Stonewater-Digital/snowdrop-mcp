---
skill: us_state_mn_fund_tax
category: fund_tax
description: Applies Minnesota top bracket approximations, composite withholding, and elective PTE tax logic under Minn. Stat.
tier: premium
inputs: none
---

# Us State Mn Fund Tax

## Description
Applies Minnesota top bracket approximations, composite withholding, and elective PTE tax logic under Minn. Stat. §§290.06 and 289A.835. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_mn_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_mn_fund_tax"`.
