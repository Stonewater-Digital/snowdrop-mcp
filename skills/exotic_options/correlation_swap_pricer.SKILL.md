---
skill: correlation_swap_pricer
category: exotic_options
description: Dispersion-style correlation swap pricer deriving the fair strike from component volatilities and index variance decomposition. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Correlation Swap Pricer

## Description
Dispersion-style correlation swap pricer deriving the fair strike from component volatilities and index variance decomposition. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "correlation_swap_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "correlation_swap_pricer"`.
