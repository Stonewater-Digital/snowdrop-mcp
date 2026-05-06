---
skill: installment_option_pricer
category: exotic_options
description: Binomial tree valuation of installment (pay-as-you-go) options with optimal abandonment before the next premium is due. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Installment Option Pricer

## Description
Binomial tree valuation of installment (pay-as-you-go) options with optimal abandonment before the next premium is due. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "installment_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "installment_option_pricer"`.
