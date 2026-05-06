---
skill: credit_mix_analyzer
category: credit
description: Analyze credit account mix by type, count diversity score, compute average account age, and provide recommendations for a healthier credit profile.
tier: free
inputs: accounts
---

# Credit Mix Analyzer

## Description
Analyze credit account mix by type, count diversity score, compute average account age, and provide recommendations for a healthier credit profile.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `accounts` | `array` | Yes | List of credit accounts. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "credit_mix_analyzer",
  "arguments": {
    "accounts": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "credit_mix_analyzer"`.
