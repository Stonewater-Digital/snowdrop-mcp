---
skill: moic_calculator
category: fund_admin
description: Computes MOIC (Multiple on Invested Capital) as total value (realized + unrealized) divided by invested capital. Also returns gain/loss in dollar terms.
tier: premium
inputs: none
---

# Moic Calculator

## Description
Computes MOIC (Multiple on Invested Capital) as total value (realized + unrealized) divided by invested capital. Also returns gain/loss in dollar terms. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "moic_calculator",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "moic_calculator"`.
