---
skill: umbrella_policy_analyzer
category: insurance
description: Analyze umbrella insurance needs: recommended coverage based on total assets minus existing liability coverage, with premium estimate.
tier: free
inputs: total_assets, existing_auto_liability, existing_home_liability
---

# Umbrella Policy Analyzer

## Description
Analyze umbrella insurance needs: recommended coverage based on total assets minus existing liability coverage, with premium estimate.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `total_assets` | `number` | Yes | Total net worth / assets to protect. |
| `existing_auto_liability` | `number` | Yes | Existing auto liability coverage limit. |
| `existing_home_liability` | `number` | Yes | Existing homeowners liability coverage limit. |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "umbrella_policy_analyzer",
  "arguments": {
    "total_assets": 0,
    "existing_auto_liability": 0,
    "existing_home_liability": 0
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "umbrella_policy_analyzer"`.
