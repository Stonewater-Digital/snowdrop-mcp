---
skill: bankruptcy_guide
category: education
description: Returns educational content on bankruptcy: Chapter 7 vs 11 vs 13, process, effects, and alternatives.
tier: free
inputs: none
---

# Bankruptcy Guide

## Description
Returns educational content on bankruptcy: Chapter 7 vs 11 vs 13, process, effects, and alternatives.

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
  "tool": "bankruptcy_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "bankruptcy_guide"`.
