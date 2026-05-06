---
skill: grant_proposal_handler
category: grants
description: Accepts, evaluates, and adjudicates Goodwill grant proposals.
tier: free
inputs: operation
---

# Grant Proposal Handler

## Description
Accepts, evaluates, and adjudicates Goodwill grant proposals.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | `string` | Yes | Action to perform: `"submit"` to create a new proposal, `"evaluate"` to score an existing one, `"adjudicate"` to approve or reject. |
| `proposal` | `object` or `null` | No | Grant proposal object. Required for `"submit"` and `"evaluate"`. Fields: `applicant` (string), `amount_usd` (float), `purpose` (string), `goodwill_score` (float, 0–10). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "grant_proposal_handler",
  "arguments": {
    "operation": "submit",
    "proposal": {
      "applicant": "Watering Hole Node #7",
      "amount_usd": 250,
      "purpose": "Open-source tooling contribution",
      "goodwill_score": 8.5
    }
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "grant_proposal_handler"`.
