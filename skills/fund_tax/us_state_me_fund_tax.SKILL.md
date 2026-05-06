---
skill: us_state_me_fund_tax
category: fund_tax
description: Calculates Maine income tax, surtax, and elective entity-level tax savings for investment funds. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Me Fund Tax

## Description
Calculates Maine income tax, surtax, and elective entity-level tax savings for investment funds. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_me_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_me_fund_tax"`.
