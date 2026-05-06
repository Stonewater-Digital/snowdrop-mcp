---
skill: monetary_policy_guide
category: education
description: Returns educational content on monetary policy: Fed tools, interest rates, quantitative easing, and inflation targeting.
tier: free
inputs: none
---

# Monetary Policy Guide

## Description
Returns educational content on monetary policy: Fed tools, interest rates, quantitative easing, and inflation targeting.

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
  "tool": "monetary_policy_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "monetary_policy_guide"`.
