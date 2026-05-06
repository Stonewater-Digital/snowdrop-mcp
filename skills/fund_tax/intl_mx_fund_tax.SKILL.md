---
skill: intl_mx_fund_tax
category: fund_tax
description: Handles Mexican withholding, capital gains rules, and the 30% corporate rate for Mexican managers. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Mx Fund Tax

## Description
Handles Mexican withholding, capital gains rules, and the 30% corporate rate for Mexican managers. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_mx_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_mx_fund_tax"`.
