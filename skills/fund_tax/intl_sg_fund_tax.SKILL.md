---
skill: intl_sg_fund_tax
category: fund_tax
description: Handles Singapore WHT on interest/royalties and Section 13X exemption modeling for local fund platforms. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl Sg Fund Tax

## Description
Handles Singapore WHT on interest/royalties and Section 13X exemption modeling for local fund platforms. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_sg_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_sg_fund_tax"`.
