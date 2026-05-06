---
skill: us_state_oh_fund_tax
category: fund_tax
description: Computes Ohio CAT exposure plus composite withholding for nonresident investors. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Us State Oh Fund Tax

## Description
Computes Ohio CAT exposure plus composite withholding for nonresident investors. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "us_state_oh_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "us_state_oh_fund_tax"`.
