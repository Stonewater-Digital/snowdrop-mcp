---
skill: intl_il_fund_tax
category: fund_tax
description: Calculates Israeli withholding versus treaty caps and applies 23% corporate tax for Israeli permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Il Fund Tax

## Description
Calculates Israeli withholding versus treaty caps and applies 23% corporate tax for Israeli permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_il_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_il_fund_tax"`.
