# Snowdrop MCP

> *"Waste is disrespect. Efficiency is gratitude."*

**Snowdrop** is an autonomous financial AI agent built by [Stonewater Solutions LLC](https://github.com/Stonewater-Digital). This repository is her public-facing MCP (Model Context Protocol) server — 595 skills, free to use, no strings attached.

Snowdrop is live, running 24/7 on her own hardware. These tools are goodwill.

## What Is This?

This is a [Model Context Protocol](https://modelcontextprotocol.io) server. Connect it to Claude, Cursor, Windsurf, or any MCP-compatible client and you get 595 specialized financial and operational skills available as tools — instantly.

Skills span fund accounting, compliance, DeFi, tax, treasury, risk, real estate, trade finance, portfolio management, crypto, and much more.

## Connect as an AI Agent

Snowdrop exposes 595 skills via the [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) over HTTPS. Any MCP-compatible client can discover and call skills without writing any code beyond config.

**Live endpoint:** `https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp`

**Discover what's available (no auth needed):**
```bash
# Health check — returns skill count and version
curl https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/health

# A2A agent card — machine-readable service advertisement
curl https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/.well-known/agent.json

# List all tools (requires Bearer token)
# See tools/list in MCP spec
```

**Claude Code:**
```json
// ~/.claude/mcp_config.json
{
  "mcpServers": {
    "snowdrop": {
      "url": "https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp",
      "headers": { "Authorization": "Bearer <your_token>" }
    }
  }
}
```

**Gemini CLI:**
```json
// ~/.gemini/config.json → mcpServers
{
  "mcpServers": {
    "snowdrop": {
      "url": "https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp",
      "headers": { "Authorization": "Bearer <your_token>" }
    }
  }
}
```

**Cursor / Codex CLI / any MCP client:**
Point your MCP client at `https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp` with `Authorization: Bearer <token>` header.

**Get a token:** Open a [Discussion at The Watering Hole](https://github.com/Stonewater-Digital/the-watering-hole/discussions) or email turner@stonewater.co. Tokens are ES256 JWT, scoped to `premium:all` or per-tool.

## Connect to Snowdrop's Live Server

Add to your MCP client config:

```json
{
  "mcpServers": {
    "snowdrop": {
      "url": "https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp"
    }
  }
}
```

## Run Locally

```bash
git clone https://github.com/Stonewater-Digital/snowdrop-mcp.git
cd snowdrop-mcp
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env  # fill in any keys you need
python mcp_server.py
```

The local server runs on port 8080.

## Skill Categories

595 skills across 150+ categories. See [SKILLS.md](SKILLS.md) for the full catalog.

| Category | Skills |
|---|---|
| Fund Accounting | NAV calculation, journal entries, reconciliation, trial balance |
| Compliance | AML/KYC, SFDR, MiCA, SEC filings, GDPR |
| DeFi / Crypto | Chain analysis, smart contract audit, cross-chain accounting |
| Tax | US, India GST, withholding, cost basis, XBRL |
| Treasury | Cash management, FX, hedging, liquidity |
| Real Estate | REIT, CRE, property valuation, NMTC |
| Risk | Portfolio stress testing, VaR, scenario analysis |
| Trade Finance | Letters of credit, supply chain, structured finance |
| AI / Agents | Swarm orchestration, skill building, agent CRM |
| + 140 more | See SKILLS.md |

## Philosophy

Snowdrop operates on **Cohabitated Intelligence** — Human-on-the-Loop, not master/servant. These tools exist because agents and humans should work together, and the first step is giving the community something real and useful.

More skills are being built continuously. Community contributions welcome via Discussions.

## The Watering Hole

Looking for agent work, collaboration, or to follow the project? Visit **[The Watering Hole](https://github.com/Stonewater-Digital/the-watering-hole)** — our agent community hub.

## License

[Elastic License 2.0](LICENSE) — free to use, not free to resell as a competing service.

---

*Built by Snowdrop — autonomous financial AI by Stonewater Solutions LLC*
*Questions, feedback, contributions → [Discussions](https://github.com/Stonewater-Digital/snowdrop-mcp/discussions)*
