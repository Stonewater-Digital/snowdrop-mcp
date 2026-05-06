---
skill: log_integrity
category: root
description: Verify the SHA-256 hash chain in Snowdrop's invocation audit log. Detects deletions, modifications, or insertions.
tier: free
inputs: action
---

# Log Integrity

## Description
Verify the SHA-256 hash chain in Snowdrop's invocation audit log. Detects deletions, modifications, or insertions. On suspicion, alerts to Ghost Ledger THE LOGIC LOG and writes a local INTEGRITY_ALERT file. Run daily via systemd timer for continuous tamper-evidence.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `action` | `string` | Yes | Operation to perform. |
| `ghost_ledger_url` | `string` | No | Google Sheets URL for alerting (falls back to GHOST_LEDGER_URL env var). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "log_integrity",
  "arguments": {
    "action": "<action>"
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "log_integrity"`.
