---
skill: intl_fr_fund_tax
category: fund_tax
description: Determines French withholding outcomes and 25% corporation tax impact when a French permanent establishment exists. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Fr Fund Tax

## Description
Determines French withholding outcomes and 25% corporation tax impact when a French permanent establishment exists. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_fr_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_fr_fund_tax"`.
