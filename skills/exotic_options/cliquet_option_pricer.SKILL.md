---
skill: cliquet_option_pricer
category: exotic_options
description: Monte Carlo pricing of locally capped/floored cliquet options with global collar following risk-neutral dynamics. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cliquet Option Pricer

## Description
Monte Carlo pricing of locally capped/floored cliquet options with global collar following risk-neutral dynamics. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cliquet_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cliquet_option_pricer"`.
