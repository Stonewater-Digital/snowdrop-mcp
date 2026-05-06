---
skill: futures_basics_guide
category: education
description: Returns educational content on futures: definition, margin, mark-to-market, hedging vs speculation.
tier: free
inputs: none
---

# Futures Basics Guide

## Description
Returns educational content on futures: definition, margin, mark-to-market, hedging vs speculation.

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
  "tool": "futures_basics_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "futures_basics_guide"`.
