---
skill: us_state_ct_fund_tax
category: fund_tax
description: Evaluates Connecticut PE Tax, nonresident withholding, and exemption status pursuant to Conn. Gen.
tier: premium
inputs: none
---

# Us State Ct Fund Tax

## Description
Evaluates Connecticut PE Tax, nonresident withholding, and exemption status pursuant to Conn. Gen. Stat. §§12-699 and 12-704d. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ct_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ct_fund_tax"`.
