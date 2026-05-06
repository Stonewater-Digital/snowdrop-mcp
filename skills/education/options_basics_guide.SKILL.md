---
skill: options_basics_guide
category: education
description: Returns educational content on options: calls/puts, intrinsic/extrinsic value, the Greeks, and basic strategies.
tier: free
inputs: none
---

# Options Basics Guide

## Description
Returns educational content on options: calls/puts, intrinsic/extrinsic value, the Greeks, and basic strategies.

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
  "tool": "options_basics_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "options_basics_guide"`.
