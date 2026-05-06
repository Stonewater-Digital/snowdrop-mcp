---
skill: intl_ca_fund_tax
category: fund_tax
description: Calculates Canadian withholding vs treaty relief and applies the 26.5% combined federal/provincial corporate rate when a Canadian permanent establishment exists. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Ca Fund Tax

## Description
Calculates Canadian withholding vs treaty relief and applies the 26.5% combined federal/provincial corporate rate when a Canadian permanent establishment exists. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_ca_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_ca_fund_tax"`.
