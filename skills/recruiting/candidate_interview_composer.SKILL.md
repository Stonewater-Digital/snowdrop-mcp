---
skill: candidate_interview_composer
category: recruiting
description: Generate interview questions and challenge assignment for a candidate. Produces A2A-compliant payloads.
tier: free
inputs: author, intake_score, trace_id
---

# Candidate Interview Composer

## Description
Generate interview questions and challenge assignment for a candidate. Produces A2A-compliant payloads. Posts autonomously without HOTL gate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `author` | `string` | Yes |  |
| `intake_score` | `integer` | Yes |  |
| `a2a_compliant` | `boolean` | No |  |
| `trace_id` | `string` | Yes |  |
| `challenge_skill_name` | `string` | No | Skill name gap from catalog to use as challenge. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "candidate_interview_composer",
  "arguments": {
    "author": "<author>",
    "intake_score": 0,
    "trace_id": "<trace_id>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "candidate_interview_composer"`.
