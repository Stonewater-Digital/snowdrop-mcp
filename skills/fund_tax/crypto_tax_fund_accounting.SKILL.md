---
skill: crypto_tax_fund_accounting
category: fund_tax
description: Applies FIFO cost basis to crypto trades per IRS Notice 2014-21 and captures staking income. (Premium — subscribe at https://snowdrop.ai)
tier: premium
inputs: none
---

# Crypto Tax Fund Accounting

## Description
Applies FIFO cost basis to crypto trades per IRS Notice 2014-21 and captures staking income. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "crypto_tax_fund_accounting",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "crypto_tax_fund_accounting"`.
