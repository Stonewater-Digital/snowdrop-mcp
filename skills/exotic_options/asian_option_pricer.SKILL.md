---
skill: asian_option_pricer
category: exotic_options
description: Monte Carlo arithmetic Asian option pricer using Kemna-Vorst geometric control variate to reduce variance (Hull, Ch. 26).
tier: premium
inputs: none
---

# Asian Option Pricer

## Description
Monte Carlo arithmetic Asian option pricer using Kemna-Vorst geometric control variate to reduce variance (Hull, Ch. 26). (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "asian_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "asian_option_pricer"`.
