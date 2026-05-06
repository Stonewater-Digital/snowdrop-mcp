---
skill: risk_management_guide
category: education
description: Returns educational content on types of financial risk, mitigation strategies, and hedging basics.
tier: free
inputs: none
---

# Risk Management Guide

## Description
Returns educational content on types of financial risk, mitigation strategies, and hedging basics.

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
  "tool": "risk_management_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "risk_management_guide"`.
