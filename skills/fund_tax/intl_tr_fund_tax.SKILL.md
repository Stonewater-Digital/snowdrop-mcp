---
skill: intl_tr_fund_tax
category: fund_tax
description: Computes Turkish withholding, treaty rates, and 25% CIT for entities with Turkish permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Tr Fund Tax

## Description
Computes Turkish withholding, treaty rates, and 25% CIT for entities with Turkish permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_tr_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_tr_fund_tax"`.
