---
skill: ipo_guide
category: education
description: Returns educational content on IPOs: process, underwriting, lock-up period, pricing, direct listing, and SPACs.
tier: free
inputs: none
---

# Ipo Guide

## Description
Returns educational content on IPOs: process, underwriting, lock-up period, pricing, direct listing, and SPACs.

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
  "tool": "ipo_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ipo_guide"`.
