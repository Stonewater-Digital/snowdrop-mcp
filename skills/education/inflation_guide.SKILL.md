---
skill: inflation_guide
category: education
description: Returns educational content on inflation: definition, CPI, causes, effects on investments, and TIPS.
tier: free
inputs: none
---

# Inflation Guide

## Description
Returns educational content on inflation: definition, CPI, causes, effects on investments, and TIPS.

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
  "tool": "inflation_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "inflation_guide"`.
