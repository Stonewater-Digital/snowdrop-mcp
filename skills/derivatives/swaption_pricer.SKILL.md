---
skill: swaption_pricer
category: derivatives
description: Prices payer or receiver swaptions via Black's model and returns Greeks. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Swaption Pricer

## Description
Prices payer or receiver swaptions via Black's model and returns Greeks. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "swaption_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "swaption_pricer"`.
