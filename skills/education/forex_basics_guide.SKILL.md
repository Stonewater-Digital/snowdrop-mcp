---
skill: forex_basics_guide
category: education
description: Returns educational content on forex: currency pairs, pips, lots, major/minor/exotic pairs.
tier: free
inputs: none
---

# Forex Basics Guide

## Description
Returns educational content on forex: currency pairs, pips, lots, major/minor/exotic pairs.

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
  "tool": "forex_basics_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "forex_basics_guide"`.
