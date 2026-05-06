---
skill: rwa_private_credit_covenant_packet_checker
category: crypto_rwa
description: Parses covenant reports to ensure breach notices trigger token gating logic.
tier: free
inputs: none
---

# Rwa Private Credit Covenant Packet Checker

## Description
Parses covenant reports to ensure breach notices trigger token gating logic.

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
  "tool": "rwa_private_credit_covenant_packet_checker",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "rwa_private_credit_covenant_packet_checker"`.
