---
skill: gdp_guide
category: education
description: Returns educational content on GDP: definition, components (C+I+G+NX), nominal vs real, and growth rate.
tier: free
inputs: none
---

# Gdp Guide

## Description
Returns educational content on GDP: definition, components (C+I+G+NX), nominal vs real, and growth rate.

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
  "tool": "gdp_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "gdp_guide"`.
