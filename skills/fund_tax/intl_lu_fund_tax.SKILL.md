---
skill: intl_lu_fund_tax
category: fund_tax
description: Models Luxembourg WHT (typically nil on interest/royalty) and local subscription tax exposure. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Lu Fund Tax

## Description
Models Luxembourg WHT (typically nil on interest/royalty) and local subscription tax exposure. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_lu_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_lu_fund_tax"`.
