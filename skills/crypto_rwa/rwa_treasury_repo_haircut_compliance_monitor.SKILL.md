---
skill: rwa_treasury_repo_haircut_compliance_monitor
category: crypto_rwa
description: Checks repo leverage agreements to ensure haircuts stay within disclosures.
tier: free
inputs: payload
---

# Rwa Treasury Repo Haircut Compliance Monitor

## Description
Checks repo leverage agreements to ensure haircuts stay within disclosures.

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
  "tool": "rwa_treasury_repo_haircut_compliance_monitor",
  "arguments": {
    "payload": "<payload>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_repo_haircut_compliance_monitor"`.
