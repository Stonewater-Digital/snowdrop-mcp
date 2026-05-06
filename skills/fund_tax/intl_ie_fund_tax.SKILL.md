---
skill: intl_ie_fund_tax
category: fund_tax
description: Evaluates Irish withholding and 12.5% trading tax for Irish fund platforms. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Ie Fund Tax

## Description
Evaluates Irish withholding and 12.5% trading tax for Irish fund platforms. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_ie_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_ie_fund_tax"`.
