---
skill: market_capitalization_guide
category: education
description: Returns educational content on market capitalization: calculation, large/mid/small cap categories, and implications.
tier: free
inputs: none
---

# Market Capitalization Guide

## Description
Returns educational content on market capitalization: calculation, large/mid/small cap categories, and implications.

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
  "tool": "market_capitalization_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "market_capitalization_guide"`.
