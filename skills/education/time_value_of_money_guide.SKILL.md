---
skill: time_value_of_money_guide
category: education
description: Returns educational content on time value of money: PV, FV, annuities, perpetuities, and discount rates.
tier: free
inputs: none
---

# Time Value Of Money Guide

## Description
Returns educational content on time value of money: PV, FV, annuities, perpetuities, and discount rates.

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
  "tool": "time_value_of_money_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "time_value_of_money_guide"`.
