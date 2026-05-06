---
skill: intl_ph_fund_tax
category: fund_tax
description: Captures Philippine withholding (including CREATE-era rates) and the domestic 25% corporate tax on Philippine permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Ph Fund Tax

## Description
Captures Philippine withholding (including CREATE-era rates) and the domestic 25% corporate tax on Philippine permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_ph_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_ph_fund_tax"`.
