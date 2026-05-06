---
skill: shout_option_pricer
category: exotic_options
description: Monte Carlo shout option valuation treating shout dates as discrete lookback checkpoints where locked intrinsic is preserved per Rubinstein's construction. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Shout Option Pricer

## Description
Monte Carlo shout option valuation treating shout dates as discrete lookback checkpoints where locked intrinsic is preserved per Rubinstein's construction. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "shout_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "shout_option_pricer"`.
