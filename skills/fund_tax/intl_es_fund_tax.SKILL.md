---
skill: intl_es_fund_tax
category: fund_tax
description: Analyzes Spanish savings tax withholding and corporate tax for Spanish managers. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Es Fund Tax

## Description
Analyzes Spanish savings tax withholding and corporate tax for Spanish managers. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_es_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_es_fund_tax"`.
