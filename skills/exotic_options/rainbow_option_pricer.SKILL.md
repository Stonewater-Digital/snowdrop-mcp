---
skill: rainbow_option_pricer
category: exotic_options
description: Monte Carlo rainbow option pricer using correlated Gaussian sampling for best-of and worst-of structures (Stulz, 1982). (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Rainbow Option Pricer

## Description
Monte Carlo rainbow option pricer using correlated Gaussian sampling for best-of and worst-of structures (Stulz, 1982). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "rainbow_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rainbow_option_pricer"`.
