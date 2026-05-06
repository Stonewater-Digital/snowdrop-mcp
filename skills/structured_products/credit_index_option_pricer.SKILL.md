---
skill: credit_index_option_pricer
category: structured_products
description: Applies Black's formula on CDS index spreads with PV01 scaling to deliver payer/receiver option values and Greeks. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Credit Index Option Pricer

## Description
Applies Black's formula on CDS index spreads with PV01 scaling to deliver payer/receiver option values and Greeks. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "credit_index_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_index_option_pricer"`.
