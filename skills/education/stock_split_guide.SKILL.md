---
skill: stock_split_guide
category: education
description: Returns educational content on stock splits: forward/reverse splits, reasons, and effects on value.
tier: free
inputs: none
---

# Stock Split Guide

## Description
Returns educational content on stock splits: forward/reverse splits, reasons, and effects on value.

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
  "tool": "stock_split_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "stock_split_guide"`.
