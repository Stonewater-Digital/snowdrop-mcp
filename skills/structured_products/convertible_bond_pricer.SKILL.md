---
skill: convertible_bond_pricer
category: structured_products
description: Approximates the Tsiveriotis-Fernandes convertible decomposition into straight bond and embedded call option to deliver price and Greeks. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Convertible Bond Pricer

## Description
Approximates the Tsiveriotis-Fernandes convertible decomposition into straight bond and embedded call option to deliver price and Greeks. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "convertible_bond_pricer",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "convertible_bond_pricer"`.
