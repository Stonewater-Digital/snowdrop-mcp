---
skill: mutual_fund_guide
category: education
description: Returns educational content on mutual funds: types, expense ratios, load vs no-load, NAV calculation.
tier: free
inputs: none
---

# Mutual Fund Guide

## Description
Returns educational content on mutual funds: types, expense ratios, load vs no-load, NAV calculation.

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
  "tool": "mutual_fund_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "mutual_fund_guide"`.
