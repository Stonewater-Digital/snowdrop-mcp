---
skill: structured_deposit_pricer
category: structured_products
description: Combines the discount cost of principal protection with the price of an embedded equity option to price structured deposits. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Structured Deposit Pricer

## Description
Combines the discount cost of principal protection with the price of an embedded equity option to price structured deposits. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "structured_deposit_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "structured_deposit_pricer"`.
