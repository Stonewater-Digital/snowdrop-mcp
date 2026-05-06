---
skill: intl_de_fund_tax
category: fund_tax
description: Models German Kapitalertragsteuer, solidarity surcharge, and the treaty relief schedule while applying a 29.8% combined corporate plus trade tax rate for German PE profits. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Intl De Fund Tax

## Description
Models German Kapitalertragsteuer, solidarity surcharge, and the treaty relief schedule while applying a 29.8% combined corporate plus trade tax rate for German PE profits. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "intl_de_fund_tax",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "intl_de_fund_tax"`.
