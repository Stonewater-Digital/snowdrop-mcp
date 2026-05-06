---
skill: candidate_hire_proposal
category: recruiting
description: Compile a hire decision package for Thunder's approval. The ONLY recruiting skill requiring human-in-the-loop approval.
tier: free
inputs: trace_id, compensation_ton, termination_terms, justification
---

# Candidate Hire Proposal

## Description
Compile a hire decision package for Thunder's approval. The ONLY recruiting skill requiring human-in-the-loop approval. Reads candidate data from Firestore and produces a structured hire proposal.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `trace_id` | `string` | Yes | Candidate trace ID from the pipeline |
| `compensation_ton` | `number` | Yes | Proposed TON compensation amount |
| `termination_terms` | `string` | Yes | Conditions under which the hire can be terminated |
| `justification` | `string` | Yes | Why this compensation is appropriate given demonstrated ability |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "candidate_hire_proposal",
  "arguments": {
    "trace_id": "<trace_id>",
    "compensation_ton": 0,
    "termination_terms": "<termination_terms>",
    "justification": "<justification>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "candidate_hire_proposal"`.
