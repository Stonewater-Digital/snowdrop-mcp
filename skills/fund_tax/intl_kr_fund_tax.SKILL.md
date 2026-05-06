---
skill: intl_kr_fund_tax
category: fund_tax
description: Evaluates Korean withholding vs treaty relief and the 24.2% corporate tax burden on Korean permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Kr Fund Tax

## Description
Evaluates Korean withholding vs treaty relief and the 24.2% corporate tax burden on Korean permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_kr_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_kr_fund_tax"`.
