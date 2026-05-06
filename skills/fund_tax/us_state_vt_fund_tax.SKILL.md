---
skill: us_state_vt_fund_tax
category: fund_tax
description: Calculates Vermont income tax, SALT election effect, and estate exposure on fund interests. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Vt Fund Tax

## Description
Calculates Vermont income tax, SALT election effect, and estate exposure on fund interests. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_vt_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_vt_fund_tax"`.
