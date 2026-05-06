---
skill: token_efficiency_benchmarker
category: crowd_economics
description: Compares tokens per skill/line/quality across internal and community contributors.
tier: free
inputs: contributions
---

# Token Efficiency Benchmarker

## Description
Compares tokens per skill/line/quality across internal and community contributors.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contributions` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "token_efficiency_benchmarker",
  "arguments": {
    "contributions": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "token_efficiency_benchmarker"`.
