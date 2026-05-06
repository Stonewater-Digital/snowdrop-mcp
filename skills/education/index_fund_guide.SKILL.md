---
skill: index_fund_guide
category: education
description: Returns educational content on index funds: passive investing, major indices, advantages, and rebalancing.
tier: free
inputs: none
---

# Index Fund Guide

## Description
Returns educational content on index funds: passive investing, major indices, advantages, and rebalancing.

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
  "tool": "index_fund_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "index_fund_guide"`.
