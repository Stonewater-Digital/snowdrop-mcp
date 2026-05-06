---
skill: us_state_id_fund_tax
category: fund_tax
description: Applies Idaho flat income tax, SALT parity election, and Form 41P withholding mechanics. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Id Fund Tax

## Description
Applies Idaho flat income tax, SALT parity election, and Form 41P withholding mechanics. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_id_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_id_fund_tax"`.
