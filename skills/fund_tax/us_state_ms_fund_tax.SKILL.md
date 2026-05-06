---
skill: us_state_ms_fund_tax
category: fund_tax
description: Handles Mississippi flat income tax, SALT election, and franchise tax exposure. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Ms Fund Tax

## Description
Handles Mississippi flat income tax, SALT election, and franchise tax exposure. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_ms_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_ms_fund_tax"`.
