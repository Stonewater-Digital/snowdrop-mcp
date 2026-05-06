---
skill: intl_ch_fund_tax
category: fund_tax
description: Computes Swiss withholding and refund potential plus cantonal/federal corporate tax on Swiss permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Ch Fund Tax

## Description
Computes Swiss withholding and refund potential plus cantonal/federal corporate tax on Swiss permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_ch_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_ch_fund_tax"`.
