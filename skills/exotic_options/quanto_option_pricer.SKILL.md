---
skill: quanto_option_pricer
category: exotic_options
description: Black-Scholes quanto pricer with correlation adjustment between asset and FX volatility (Hull, Ch. 28).
tier: premium
inputs: none
---

# Quanto Option Pricer

## Description
Black-Scholes quanto pricer with correlation adjustment between asset and FX volatility (Hull, Ch. 28). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "quanto_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "quanto_option_pricer"`.
