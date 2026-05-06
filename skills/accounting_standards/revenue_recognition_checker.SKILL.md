---
skill: revenue_recognition_checker
category: accounting_standards
description: Applies the ASC 606 five-step model to contracts and allocates revenue to obligations.
tier: free
inputs: contract
---

# Revenue Recognition Checker

## Description
Applies the ASC 606 five-step model to contracts and allocates revenue to obligations.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `contract` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "revenue_recognition_checker",
  "arguments": {
    "contract": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "revenue_recognition_checker"`.
