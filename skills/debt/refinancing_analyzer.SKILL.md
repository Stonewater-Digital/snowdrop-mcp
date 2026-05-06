---
skill: refinancing_analyzer
category: debt
description: Evaluates refinance savings, break-even, and NPV for proposed loan terms.
tier: free
inputs: current_loan, proposed_loan
---

# Refinancing Analyzer

## Description
Evaluates refinance savings, break-even, and NPV for proposed loan terms.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_loan` | `object` | Yes |  |
| `proposed_loan` | `object` | Yes |  |
| `discount_rate` | `number` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "refinancing_analyzer",
  "arguments": {
    "current_loan": {},
    "proposed_loan": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "refinancing_analyzer"`.
