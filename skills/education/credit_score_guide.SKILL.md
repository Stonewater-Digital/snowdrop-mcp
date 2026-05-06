---
skill: credit_score_guide
category: education
description: Returns educational content on credit scores: FICO ranges, scoring factors, and improvement tips.
tier: free
inputs: none
---

# Credit Score Guide

## Description
Returns educational content on credit scores: FICO ranges, scoring factors, and improvement tips.

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
  "tool": "credit_score_guide",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_score_guide"`.
