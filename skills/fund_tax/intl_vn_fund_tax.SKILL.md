---
skill: intl_vn_fund_tax
category: fund_tax
description: Provides Vietnam foreign contractor tax computations and 20% corporate tax for onshore subsidiaries. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Vn Fund Tax

## Description
Provides Vietnam foreign contractor tax computations and 20% corporate tax for onshore subsidiaries. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_vn_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_vn_fund_tax"`.
