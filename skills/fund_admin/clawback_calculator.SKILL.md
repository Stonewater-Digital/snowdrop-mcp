---
skill: clawback_calculator
category: fund_admin
description: Determines GP clawback due when interim carried interest distributions exceed final entitlement. Optionally applies interest on the outstanding clawback amount.
tier: premium
inputs: none
---

# Clawback Calculator

## Description
Determines GP clawback due when interim carried interest distributions exceed final entitlement. Optionally applies interest on the outstanding clawback amount. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "clawback_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "clawback_calculator"`.
