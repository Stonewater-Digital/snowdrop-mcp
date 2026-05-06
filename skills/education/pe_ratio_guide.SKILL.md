---
skill: pe_ratio_guide
category: education
description: Returns educational content on P/E ratio: formula, forward vs trailing, sector averages, and PEG ratio.
tier: free
inputs: none
---

# Pe Ratio Guide

## Description
Returns educational content on P/E ratio: formula, forward vs trailing, sector averages, and PEG ratio.

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
  "tool": "pe_ratio_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "pe_ratio_guide"`.
