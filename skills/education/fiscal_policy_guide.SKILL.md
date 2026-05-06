---
skill: fiscal_policy_guide
category: education
description: Returns educational content on fiscal policy: taxation, government spending, deficits, and the multiplier effect.
tier: free
inputs: none
---

# Fiscal Policy Guide

## Description
Returns educational content on fiscal policy: taxation, government spending, deficits, and the multiplier effect.

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
  "tool": "fiscal_policy_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "fiscal_policy_guide"`.
