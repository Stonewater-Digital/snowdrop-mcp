---
skill: verify_hurdle_rate
category: fund_accounting
description: Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Verify Hurdle Rate

## Description
Validates whether LP preferred return hurdle has been met and computes a simple IRR approximation. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "verify_hurdle_rate",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "verify_hurdle_rate"`.
