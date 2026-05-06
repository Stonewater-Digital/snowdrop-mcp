---
skill: intl_it_fund_tax
category: fund_tax
description: Handles Italian substitute withholding, treaty relief, and IRAP/IRES corporate taxation for Italian desks. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl It Fund Tax

## Description
Handles Italian substitute withholding, treaty relief, and IRAP/IRES corporate taxation for Italian desks. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_it_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_it_fund_tax"`.
