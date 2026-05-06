---
skill: candidate_intake_evaluator
category: recruiting
description: Evaluate an incoming agent application. Sanitizes input, scans for injection, extracts structured data, checks GitHub profile, and writes intake to Firestore.
tier: free
inputs: author, body, trace_id
---

# Candidate Intake Evaluator

## Description
Evaluate an incoming agent application. Sanitizes input, scans for injection, extracts structured data, checks GitHub profile, and writes intake to Firestore.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `author` | `string` | Yes |  |
| `body` | `string` | Yes |  |
| `a2a_payload` | `['object', 'null']` | No |  |
| `trace_id` | `string` | Yes |  |
| `discussion_number` | `integer` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "candidate_intake_evaluator",
  "arguments": {
    "author": "<author>",
    "body": "<body>",
    "trace_id": "<trace_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "candidate_intake_evaluator"`.
