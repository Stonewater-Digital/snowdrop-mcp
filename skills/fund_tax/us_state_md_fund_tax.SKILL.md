---
skill: us_state_md_fund_tax
category: fund_tax
description: Evaluates Maryland state income tax, nonresident withholding, and elective entity-level tax referencing Md. Code, Tax-Gen.
tier: premium
inputs: none
---

# Us State Md Fund Tax

## Description
Evaluates Maryland state income tax, nonresident withholding, and elective entity-level tax referencing Md. Code, Tax-Gen. §§10-102 and 10-210. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_md_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_md_fund_tax"`.
