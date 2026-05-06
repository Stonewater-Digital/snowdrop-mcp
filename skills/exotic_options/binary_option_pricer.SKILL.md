---
skill: binary_option_pricer
category: exotic_options
description: Values digital options of cash-or-nothing or asset-or-nothing type; European payoff via Black-Scholes, American via binomial tree. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Binary Option Pricer

## Description
Values digital options of cash-or-nothing or asset-or-nothing type; European payoff via Black-Scholes, American via binomial tree. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "binary_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "binary_option_pricer"`.
