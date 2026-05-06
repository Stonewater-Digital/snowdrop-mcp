---
skill: kyc_aml_chain_analysis
category: compliance
description: Performs on-chain KYC/AML screening by cross-referencing wallet addresses against OFAC-style sanctioned address lists and heuristic risk indicators including mixer usage patterns, rapid fund movement (under 24h), and known bad actor address clusters. Supports TON, Solana, and Ethereum chains.
tier: premium
inputs: none
---

# Kyc Aml Chain Analysis

## Description
Performs on-chain KYC/AML screening by cross-referencing wallet addresses against OFAC-style sanctioned address lists and heuristic risk indicators including mixer usage patterns, rapid fund movement (under 24h), and known bad actor address clusters. Supports TON, Solana, and Ethereum chains. (Premium — subscribe at https://snowdrop.ai)

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
  "tool": "kyc_aml_chain_analysis",
  "arguments": {}
}
```

## Usage
Invoke via `snowdrop_execute` with `tool_name: "kyc_aml_chain_analysis"`.
