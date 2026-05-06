---
skill: compound_option_pricer
category: exotic_options
description: Geske (1979) closed-form pricer for call-on-call and put-on-call compound options using bivariate normals. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Compound Option Pricer

## Description
Geske (1979) closed-form pricer for call-on-call and put-on-call compound options using bivariate normals. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "compound_option_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compound_option_pricer"`.
