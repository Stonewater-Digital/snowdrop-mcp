---
skill: us_state_fl_fund_tax
category: fund_tax
description: Determines Florida corporate income/franchise tax exposure for hedge fund management entities while noting pass-through exemption for entities that remain partnerships. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Fl Fund Tax

## Description
Determines Florida corporate income/franchise tax exposure for hedge fund management entities while noting pass-through exemption for entities that remain partnerships. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_fl_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_fl_fund_tax"`.
