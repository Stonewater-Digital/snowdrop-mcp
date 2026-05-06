---
skill: loan_amendment_tracker
category: private_credit
description: Scores cumulative impact of loan amendments to highlight covenant drift.
tier: free
inputs: amendments
---

# Loan Amendment Tracker

## Description
Scores cumulative impact of loan amendments to highlight covenant drift.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `amendments` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "loan_amendment_tracker",
  "arguments": {
    "amendments": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "loan_amendment_tracker"`.
