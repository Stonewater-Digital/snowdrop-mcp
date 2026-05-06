---
skill: ebitda_addback_analyzer
category: private_credit
description: Scores EBITDA addbacks by quality to show normalized EBITDA.
tier: free
inputs: base_ebitda, addbacks
---

# Ebitda Addback Analyzer

## Description
Scores EBITDA addbacks by quality to show normalized EBITDA.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `base_ebitda` | `number` | Yes |  |
| `addbacks` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "ebitda_addback_analyzer",
  "arguments": {
    "base_ebitda": 0,
    "addbacks": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "ebitda_addback_analyzer"`.
