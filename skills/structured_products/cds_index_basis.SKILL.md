---
skill: cds_index_basis
category: structured_products
description: Measures the difference between traded CDS index spread and the weighted intrinsic spread and derives implied correlation using variance decomposition. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Cds Index Basis

## Description
Measures the difference between traded CDS index spread and the weighted intrinsic spread and derives implied correlation using variance decomposition. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "cds_index_basis",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "cds_index_basis"`.
