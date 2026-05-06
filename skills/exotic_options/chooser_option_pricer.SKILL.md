---
skill: chooser_option_pricer
category: exotic_options
description: Rubinstein chooser pricing via combination of Black-Scholes call and adjusted put legs, supporting standard and complex choosers. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Chooser Option Pricer

## Description
Rubinstein chooser pricing via combination of Black-Scholes call and adjusted put legs, supporting standard and complex choosers. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "chooser_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "chooser_option_pricer"`.
