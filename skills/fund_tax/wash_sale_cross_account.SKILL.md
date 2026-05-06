---
skill: wash_sale_cross_account
category: fund_tax
description: Determines wash-sale disallowances when substantially identical securities are repurchased within ±30 days across related accounts. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Wash Sale Cross Account

## Description
Determines wash-sale disallowances when substantially identical securities are repurchased within ±30 days across related accounts. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "wash_sale_cross_account",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "wash_sale_cross_account"`.
