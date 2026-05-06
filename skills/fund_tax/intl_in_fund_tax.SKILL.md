---
skill: intl_in_fund_tax
category: fund_tax
description: Handles Indian Section 195 withholding, FPI capital gains, and local corporate tax when India permanent establishments exist. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl In Fund Tax

## Description
Handles Indian Section 195 withholding, FPI capital gains, and local corporate tax when India permanent establishments exist. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_in_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_in_fund_tax"`.
