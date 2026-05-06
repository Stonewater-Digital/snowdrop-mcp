---
skill: compound_interest_guide
category: education
description: Returns educational content on compound interest: formula, Rule of 72, compounding frequencies, and examples.
tier: free
inputs: none
---

# Compound Interest Guide

## Description
Returns educational content on compound interest: formula, Rule of 72, compounding frequencies, and examples.

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
  "tool": "compound_interest_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "compound_interest_guide"`.
