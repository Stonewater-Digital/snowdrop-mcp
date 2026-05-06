---
skill: spread_option_pricer
category: exotic_options
description: Computes two-asset spread option values via Kirk's approximation and correlated Monte Carlo for verification. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Spread Option Pricer

## Description
Computes two-asset spread option values via Kirk's approximation and correlated Monte Carlo for verification. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "spread_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "spread_option_pricer"`.
