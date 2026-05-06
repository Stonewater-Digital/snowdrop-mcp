---
skill: intl_za_fund_tax
category: fund_tax
description: Assesses South African dividend/interest withholding, CGT inclusion, and 27% corporate tax for local operations. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Za Fund Tax

## Description
Assesses South African dividend/interest withholding, CGT inclusion, and 27% corporate tax for local operations. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_za_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_za_fund_tax"`.
