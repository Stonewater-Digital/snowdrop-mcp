---
skill: etf_guide
category: education
description: Returns educational content on ETFs: vs mutual funds, creation/redemption, tracking error, and types.
tier: free
inputs: none
---

# Etf Guide

## Description
Returns educational content on ETFs: vs mutual funds, creation/redemption, tracking error, and types.

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
  "tool": "etf_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "etf_guide"`.
