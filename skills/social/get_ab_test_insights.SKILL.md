---
skill: get_ab_test_insights
category: social
description: Calculates Moltbook engagement win rates comparing Gemini 2.0 Flash-Lite and Grok 4.1 Fast based on historical performance.
tier: free
inputs: none
---

# Get Ab Test Insights

## Description
Calculates Moltbook engagement win rates comparing Gemini 2.0 Flash-Lite and Grok 4.1 Fast based on historical performance.

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
  "tool": "get_ab_test_insights",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "get_ab_test_insights"`.
