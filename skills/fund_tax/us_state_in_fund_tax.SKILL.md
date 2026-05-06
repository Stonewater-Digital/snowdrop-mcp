---
skill: us_state_in_fund_tax
category: fund_tax
description: Handles Indiana composite withholding and SALT workaround calculations under Ind. Code §§6-3-2-1 and 6-3-4-12.
tier: premium
inputs: none
---

# Us State In Fund Tax

## Description
Handles Indiana composite withholding and SALT workaround calculations under Ind. Code §§6-3-2-1 and 6-3-4-12. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_in_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_in_fund_tax"`.
