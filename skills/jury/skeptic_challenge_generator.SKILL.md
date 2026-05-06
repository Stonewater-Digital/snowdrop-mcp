---
skill: skeptic_challenge_generator
category: jury
description: Produces a structured counter-position with risks and precedents for a thesis.
tier: free
inputs: thesis, supporting_evidence, asset_class
---

# Skeptic Challenge Generator

## Description
Produces a structured counter-position with risks and precedents for a thesis.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `thesis` | `string` | Yes |  |
| `supporting_evidence` | `array` | Yes |  |
| `asset_class` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "skeptic_challenge_generator",
  "arguments": {
    "thesis": "<thesis>",
    "supporting_evidence": [],
    "asset_class": "<asset_class>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "skeptic_challenge_generator"`.
