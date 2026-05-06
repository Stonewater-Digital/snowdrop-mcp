---
skill: allocation_enforcer_80_20
category: fund_accounting
description: Ensures the Snowdrop portfolio stays within the 80/20 ±5% guardrails. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Allocation Enforcer 80 20

## Description
Ensures the Snowdrop portfolio stays within the 80/20 ±5% guardrails. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "allocation_enforcer_80_20",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "allocation_enforcer_80_20"`.
