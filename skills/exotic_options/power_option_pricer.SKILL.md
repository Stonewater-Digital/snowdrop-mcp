---
skill: power_option_pricer
category: exotic_options
description: Closed-form pricing for type-I power options (payoff (S^n − K)^+) based on moment-adjusted Black-Scholes. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Power Option Pricer

## Description
Closed-form pricing for type-I power options (payoff (S^n − K)^+) based on moment-adjusted Black-Scholes. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "power_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "power_option_pricer"`.
