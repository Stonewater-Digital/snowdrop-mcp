---
skill: stock_valuation_guide
category: education
description: Returns educational content on stock valuation methods: DCF, P/E, P/B, DDM with usage guidance and limitations.
tier: free
inputs: none
---

# Stock Valuation Guide

## Description
Returns educational content on stock valuation methods: DCF, P/E, P/B, DDM with usage guidance and limitations.

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
  "tool": "stock_valuation_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stock_valuation_guide"`.
