---
skill: lookback_option_pricer
category: exotic_options
description: Monte Carlo valuation of fixed or floating strike lookback options by monitoring running extrema (Glasserman, 2003). (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Lookback Option Pricer

## Description
Monte Carlo valuation of fixed or floating strike lookback options by monitoring running extrema (Glasserman, 2003). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "lookback_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "lookback_option_pricer"`.
