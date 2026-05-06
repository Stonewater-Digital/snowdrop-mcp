---
skill: us_state_mo_fund_tax
category: fund_tax
description: Estimates Missouri tax, elective entity-level tax, and Form MO-2NR withholding per Mo. Rev.
tier: premium
inputs: none
---

# Us State Mo Fund Tax

## Description
Estimates Missouri tax, elective entity-level tax, and Form MO-2NR withholding per Mo. Rev. Stat. §§143.011 and 143.441. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_mo_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_mo_fund_tax"`.
