---
skill: rwa_concentration_risk_analyzer
category: rwa_tokenization
description: Calculates concentration metrics for tokenized asset pools by asset type or geography.
tier: free
inputs: exposures
---

# Rwa Concentration Risk Analyzer

## Description
Calculates concentration metrics for tokenized asset pools by asset type or geography.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `exposures` | `array` | Yes | Exposure by bucket |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_concentration_risk_analyzer",
  "arguments": {
    "exposures": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_concentration_risk_analyzer"`.
