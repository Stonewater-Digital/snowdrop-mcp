---
skill: smart_contract_access_control_diff_checker
category: crypto_rwa
description: Diffs access-control lists between versions to highlight missing roles.
tier: free
inputs: payload
---

# Smart Contract Access Control Diff Checker

## Description
Diffs access-control lists between versions to highlight missing roles.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `payload` | `any` | Yes |  |
| `context` | `any` | No |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "smart_contract_access_control_diff_checker",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "smart_contract_access_control_diff_checker"`.
