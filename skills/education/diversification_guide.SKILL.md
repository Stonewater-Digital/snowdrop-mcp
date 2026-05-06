---
skill: diversification_guide
category: education
description: Returns educational content on diversification: asset classes, correlation, rebalancing, and international diversification.
tier: free
inputs: none
---

# Diversification Guide

## Description
Returns educational content on diversification: asset classes, correlation, rebalancing, and international diversification.

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
  "tool": "diversification_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "diversification_guide"`.
