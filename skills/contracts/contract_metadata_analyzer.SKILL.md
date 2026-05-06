---
skill: contract_metadata_analyzer
category: contracts
description: Scores contract risk based on verification, usage, and deployer reputation.
tier: free
inputs: address, chain, metadata
---

# Contract Metadata Analyzer

## Description
Scores contract risk based on verification, usage, and deployer reputation.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `address` | `string` | Yes |  |
| `chain` | `string` | Yes |  |
| `metadata` | `object` | Yes |  |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "contract_metadata_analyzer",
  "arguments": {
    "address": "<address>",
    "chain": "<chain>",
    "metadata": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "contract_metadata_analyzer"`.
