---
skill: investment_basics_explainer
category: education
description: Returns plain-language explanations for foundational investing topics.
tier: free
inputs: concept
---

# Investment Basics Explainer

## Description
Returns plain-language explanations for foundational investing topics.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `concept` | `string` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "investment_basics_explainer",
  "arguments": {
    "concept": "<concept>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "investment_basics_explainer"`.
