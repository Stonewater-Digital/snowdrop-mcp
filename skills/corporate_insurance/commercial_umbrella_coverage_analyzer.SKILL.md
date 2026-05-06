---
skill: commercial_umbrella_coverage_analyzer
category: corporate_insurance
description: Determines umbrella exhaustion probabilities and gap coverage.
tier: free
inputs: primary_layers, umbrella_limit, loss_curve
---

# Commercial Umbrella Coverage Analyzer

## Description
Determines umbrella exhaustion probabilities and gap coverage.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `primary_layers` | `array` | Yes |  |
| `umbrella_limit` | `number` | Yes |  |
| `loss_curve` | `array` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "commercial_umbrella_coverage_analyzer",
  "arguments": {
    "primary_layers": [],
    "umbrella_limit": 0,
    "loss_curve": []
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "commercial_umbrella_coverage_analyzer"`.
