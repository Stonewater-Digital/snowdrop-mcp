---
skill: intl_gb_fund_tax
category: fund_tax
description: Assesses UK withholding under ITA 2007 and the US-UK treaty while modeling 25% corporation tax on UK permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Gb Fund Tax

## Description
Assesses UK withholding under ITA 2007 and the US-UK treaty while modeling 25% corporation tax on UK permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_gb_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_gb_fund_tax"`.
