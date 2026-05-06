---
skill: barrier_option_pricer
category: exotic_options
description: Monte Carlo pricer for continuously monitored barriers using Brownian-bridge correction (Broadie-Glasserman, 1997) for up/down and in/out configurations. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Barrier Option Pricer

## Description
Monte Carlo pricer for continuously monitored barriers using Brownian-bridge correction (Broadie-Glasserman, 1997) for up/down and in/out configurations. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "barrier_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "barrier_option_pricer"`.
