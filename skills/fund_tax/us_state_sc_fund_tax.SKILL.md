---
skill: us_state_sc_fund_tax
category: fund_tax
description: Handles South Carolina nonresident withholding and elective entity-level tax calculations under S.C. Code §§12-6-510 and 12-6-590.
tier: premium
inputs: none
---

# Us State Sc Fund Tax

## Description
Handles South Carolina nonresident withholding and elective entity-level tax calculations under S.C. Code §§12-6-510 and 12-6-590. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_sc_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_sc_fund_tax"`.
