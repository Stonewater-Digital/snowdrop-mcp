---
skill: bond_basics_guide
category: education
description: Returns educational content on bond fundamentals: definition, types, key terms, and pricing basics.
tier: free
inputs: none
---

# Bond Basics Guide

## Description
Returns educational content on bond fundamentals: definition, types, key terms, and pricing basics.

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
  "tool": "bond_basics_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bond_basics_guide"`.
