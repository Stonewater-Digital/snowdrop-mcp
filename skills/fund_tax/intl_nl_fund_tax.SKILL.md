---
skill: intl_nl_fund_tax
category: fund_tax
description: Computes Dutch dividend WHT and conditional WHT while applying the 25.8% CIT for Dutch permanent establishments. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Nl Fund Tax

## Description
Computes Dutch dividend WHT and conditional WHT while applying the 25.8% CIT for Dutch permanent establishments. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_nl_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_nl_fund_tax"`.
