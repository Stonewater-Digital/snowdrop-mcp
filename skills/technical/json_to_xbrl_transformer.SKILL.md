---
skill: json_to_xbrl_transformer
category: technical
description: Transform JSON financial facts into SEC XBRL-JSON format using the us-gaap taxonomy. Maps concept names to us-gaap namespace and generates inline XBRL-compatible output.
tier: free
inputs: financial_data
---

# Json To Xbrl Transformer

## Description
Transform JSON financial facts into SEC XBRL-JSON format using the us-gaap taxonomy. Maps concept names to us-gaap namespace and generates inline XBRL-compatible output.

## Parameters
| Name | Type | Required | Description |
|------|------|----------|-------------|
| `financial_data` | `object` | Yes | Financial data dict with: entity_name (str), cik (str), period (str, e.g. '2025-12-31'), facts (dict mapping concept name → numeric value). |

## Returns
Standard Snowdrop envelope:
```json
{"status": "ok"|"error", "data": {...}, "timestamp": "ISO8601"}
```

## Example
```json
{
  "tool": "json_to_xbrl_transformer",
  "arguments": {
    "financial_data": {}
  }
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "json_to_xbrl_transformer"`.
