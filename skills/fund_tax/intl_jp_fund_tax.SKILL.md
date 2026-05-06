---
skill: intl_jp_fund_tax
category: fund_tax
description: Calculates Japanese WHT (20.315% standard) vs US treaty reductions and applies the 30.5% corporation tax to Japanese permanent establishment profits. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Jp Fund Tax

## Description
Calculates Japanese WHT (20.315% standard) vs US treaty reductions and applies the 30.5% corporation tax to Japanese permanent establishment profits. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_jp_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_jp_fund_tax"`.
