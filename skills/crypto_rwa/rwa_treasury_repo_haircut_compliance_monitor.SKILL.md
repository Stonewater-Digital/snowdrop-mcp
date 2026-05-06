---
skill: rwa_treasury_repo_haircut_compliance_monitor
category: crypto_rwa
description: Checks repo leverage agreements to ensure haircuts stay within disclosures.
tier: free
inputs: none
---

# Rwa Treasury Repo Haircut Compliance Monitor

## Description
Checks repo leverage agreements to ensure haircuts stay within disclosures.

## Parameters
_No parameters defined._

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "rwa_treasury_repo_haircut_compliance_monitor",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_treasury_repo_haircut_compliance_monitor"`.
