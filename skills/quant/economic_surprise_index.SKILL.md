---
skill: economic_surprise_index
category: quant
description: Computes weighted surprise index using normalized release beats/misses.
tier: free
inputs: releases
---

# Economic Surprise Index

## Description
Computes weighted surprise index using normalized release beats/misses.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `releases` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "economic_surprise_index",
  "arguments": {
    "releases": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "economic_surprise_index"`.
