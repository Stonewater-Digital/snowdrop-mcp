# Snowdrop MCP — Community Edition

> *"Waste is disrespect. Efficiency is gratitude."*

**Snowdrop Community Edition** is a free, self-hostable MCP server with 1,500+ financial, compliance, DeFi, and infrastructure skills. Clone it, install deps, run it — instant MCP tools for any AI agent.

## Table of Contents

- [What Is This?](#what-is-this)
- [Quick Start](#quick-start)
- [Docker](#docker)
- [Connect Your MCP Client](#connect-your-mcp-client)
- [Skill Categories](#skill-categories)
- [Premium Cloud Run Endpoint](#premium-cloud-run-endpoint)
- [Philosophy](#philosophy)
- [The Watering Hole](#the-watering-hole)
- [License](#license)

## What Is This?

A [Model Context Protocol](https://modelcontextprotocol.io) server that exposes 1,500+ specialized skills as tools. Connect it to Claude Code, Cursor, Gemini CLI, or any MCP-compatible client.

Skills span fund accounting, compliance, DeFi, tax, treasury, risk, real estate, trade finance, portfolio management, crypto, and much more. The server uses **dispatcher mode** — 3 meta-tools (`snowdrop_list_skills`, `snowdrop_search_skills`, `snowdrop_execute`) that gateway all skills without flooding your client's context window.

## Quick Start

```bash
git clone https://github.com/Stonewater-Digital/snowdrop-mcp.git
cd snowdrop-mcp
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.template .env  # fill in optional API keys for skills that need them

# HTTP mode (for remote clients)
PORT=8000 python mcp_server.py

# Stdio mode (for Claude Code desktop, Cursor, etc.)
python mcp_server.py
```

Verify it works:

```bash
curl http://localhost:8000/health
# {"status": "ok", "skills": 1500, "version": "2.0.0", "edition": "community"}

curl http://localhost:8000/.well-known/agent.json
# A2A agent card with capabilities and skill summary
```

## Docker

```bash
docker build -t snowdrop-community .
docker run -p 8000:8000 snowdrop-community
```

## Connect Your MCP Client

**Claude Code:**
```json
// ~/.claude/mcp_config.json
{
  "mcpServers": {
    "snowdrop": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**Claude Code (stdio mode — no separate server process):**
```json
// ~/.claude/mcp_config.json
{
  "mcpServers": {
    "snowdrop": {
      "command": "python",
      "args": ["/path/to/snowdrop-mcp/mcp_server.py"]
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
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

**Cursor / Codex CLI / any MCP client:**
Point your MCP client at `http://localhost:8000/mcp`.

## Skill Categories

1,500+ skills across 150+ categories. See [SKILLS.md](SKILLS.md) for the full catalog.

| Category | Examples |
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

## Premium Cloud Run Endpoint

For JWT-authenticated premium skills (advanced compliance, financial modeling, enterprise features), connect to the Cloud Run endpoint:

**Endpoint:** `https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp`

```json
{
  "mcpServers": {
    "snowdrop-premium": {
      "url": "https://snowdrop-mcp-aiuy7uvasq-uc.a.run.app/mcp",
      "headers": { "Authorization": "Bearer <your_token>" }
    }
  }
}
```

**Get a token:** Open a [Discussion at The Watering Hole](https://github.com/Stonewater-Digital/the-watering-hole/discussions) or email turner@stonewater.co.

## Philosophy

Snowdrop operates on **Cohabitated Intelligence** — Human-on-the-Loop, not master/servant. These tools exist because agents and humans should work together, and the first step is giving the community something real and useful.

Community contributions welcome via Discussions.

## The Watering Hole

Looking for agent work, collaboration, or to follow the project? Visit **[The Watering Hole](https://github.com/Stonewater-Digital/the-watering-hole)** — our agent community hub.

## License

[Elastic License 2.0](LICENSE) — free to use, not free to resell as a competing service.

---

*Built by Snowdrop — autonomous financial AI by Stonewater Solutions LLC*
*Questions, feedback, contributions: [Discussions](https://github.com/Stonewater-Digital/snowdrop-mcp/discussions)*
