---
skill: intl_hk_fund_tax
category: fund_tax
description: Provides Hong Kong profits tax modeling and notes absence of treaty relief for US investors. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Hk Fund Tax

## Description
Provides Hong Kong profits tax modeling and notes absence of treaty relief for US investors. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_hk_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_hk_fund_tax"`.
