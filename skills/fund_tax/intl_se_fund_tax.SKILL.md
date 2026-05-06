---
skill: intl_se_fund_tax
category: fund_tax
description: Computes Swedish dividend withholding, treaty relief, and the 20.6% corporate tax on Swedish permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Se Fund Tax

## Description
Computes Swedish dividend withholding, treaty relief, and the 20.6% corporate tax on Swedish permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_se_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_se_fund_tax"`.
