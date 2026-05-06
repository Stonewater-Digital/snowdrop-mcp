---
skill: option_pool_modeler
category: venture
description: Evaluates current and proposed option pool sizing plus dilution to shareholders. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Option Pool Modeler

## Description
Evaluates current and proposed option pool sizing plus dilution to shareholders. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "option_pool_modeler",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "option_pool_modeler"`.
