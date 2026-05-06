---
skill: private_credit_term_analyzer
category: private_credit
description: Computes all-in yields, covenant protection, and risk assessment for private credit facilities.
tier: free
inputs: facility
---

# Private Credit Term Analyzer

## Description
Computes all-in yields, covenant protection, and risk assessment for private credit facilities.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `facility` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "private_credit_term_analyzer",
  "arguments": {
    "facility": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "private_credit_term_analyzer"`.
