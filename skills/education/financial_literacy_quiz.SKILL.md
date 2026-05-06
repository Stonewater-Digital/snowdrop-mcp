---
skill: financial_literacy_quiz
category: education
description: Provides educational quizzes for goodwill content.
tier: free
inputs: difficulty
---

# Financial Literacy Quiz

## Description
Provides educational quizzes for goodwill content.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `difficulty` | `string` | Yes |  |
| `topic` | `string` | No |  |
| `num_questions` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "financial_literacy_quiz",
  "arguments": {
    "difficulty": "<difficulty>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "financial_literacy_quiz"`.
