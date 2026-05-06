---
skill: brexit_passporting_check
category: compliance
description: Post-Brexit cross-border licensing analysis for UK and EU financial services. Confirms that EEA passporting is definitively unavailable since 31 December 2020, evaluates available equivalence decisions, and determines local authorisation requirements per target market and licence type.
tier: premium
inputs: none
---

# Brexit Passporting Check

## Description
Post-Brexit cross-border licensing analysis for UK and EU financial services. Confirms that EEA passporting is definitively unavailable since 31 December 2020, evaluates available equivalence decisions, and determines local authorisation requirements per target market and licence type. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "brexit_passporting_check",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "brexit_passporting_check"`.
