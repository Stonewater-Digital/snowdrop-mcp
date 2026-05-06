---
skill: intl_co_fund_tax
category: fund_tax
description: Models Colombian withholding without treaty protection and applies the 35% corporate rate (20% for FTZ) to local PE income. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Co Fund Tax

## Description
Models Colombian withholding without treaty protection and applies the 35% corporate rate (20% for FTZ) to local PE income. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_co_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_co_fund_tax"`.
