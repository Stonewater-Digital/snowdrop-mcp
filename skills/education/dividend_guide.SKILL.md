---
skill: dividend_guide
category: education
description: Returns educational content on dividends: types, key dates, yield, payout ratio, and DRIP.
tier: free
inputs: none
---

# Dividend Guide

## Description
Returns educational content on dividends: types, key dates, yield, payout ratio, and DRIP.

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
  "tool": "dividend_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "dividend_guide"`.
