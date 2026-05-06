---
skill: intl_th_fund_tax
category: fund_tax
description: Computes Thai withholding, treaty reductions, and 20% corporate tax for Bangkok management entities. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Th Fund Tax

## Description
Computes Thai withholding, treaty reductions, and 20% corporate tax for Bangkok management entities. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_th_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_th_fund_tax"`.
