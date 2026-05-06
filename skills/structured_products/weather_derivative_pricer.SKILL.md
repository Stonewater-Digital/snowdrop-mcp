---
skill: weather_derivative_pricer
category: structured_products
description: Converts historical temperatures into HDD/CDD indices, computes expected payout, and delivers burn analysis statistics. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Weather Derivative Pricer

## Description
Converts historical temperatures into HDD/CDD indices, computes expected payout, and delivers burn analysis statistics. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "weather_derivative_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "weather_derivative_pricer"`.
