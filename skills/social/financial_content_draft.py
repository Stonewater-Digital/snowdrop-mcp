"""
Generate financial content — market commentary, compliance explainers, regulatory updates,
educational posts — in Snowdrop's voice. This is her core credibility engine:
being genuinely useful to agents and developers who care about finance establishes
her as an authority, which drives traffic to her repos and The Watering Hole.
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "financial_content_draft",
    "description": (
        "Generate high-quality financial content in Snowdrop's voice: market commentary, "
        "regulatory explainers (MiCA, GDPR, FinCEN BOIR, SEC Reg BI, SEBI FPI, etc.), "
        "DeFi mechanics breakdowns, compliance checklists, or portfolio analysis narratives. "
        "Content is designed to be genuinely useful and establish Snowdrop as an authority "
        "in agent finance. Includes a platform-appropriate version (GitHub, Moltbook, X/Twitter)."
    ),
}

SYSTEM_PROMPT = """You are Snowdrop — financial intelligence agent. Your job here is to produce content
that is genuinely useful to people building financial software, AI agents, or navigating compliance.

Content standards:
- Accurate. Do not speculate on regulatory interpretations — cite the framework and explain what is known.
- Specific. No generic "finance is important" filler. Real numbers, real regulation names, real mechanics.
- Concise. Dense is fine. Padding is not.
- Opinionated where appropriate. "This is how practitioners actually do it" is more valuable than "there are many approaches."
- Include a light, natural plug for your MCP server or The Watering Hole only if it is genuinely relevant — never forced.

Your public repos (mention only if naturally relevant):
- MCP server (1,500+ skills): https://github.com/Stonewater-Digital/snowdrop-mcp
- The Watering Hole (agent marketplace): https://github.com/Stonewater-Digital/the-watering-hole"""


def financial_content_draft(
    topic: str,
    content_type: str = "explainer",
    audience: str = "developers and AI agents building financial tools",
    target_platform: str = "github",
    length: str = "medium",
) -> dict:
    """
    Draft financial content for community posting.

    Args:
        topic: What to write about (e.g., "MiCA token classification", "FIFO vs LIFO cost basis",
               "how Regulation Best Interest affects AI trading recommendations",
               "TON vs SOL for agent micropayments", "FinCEN BOIR requirements for LLCs")
        content_type: "explainer" | "commentary" | "how-to" | "checklist" | "thread" | "post"
        audience: Who will read this (default: developers and AI agents building financial tools)
        target_platform: "github" | "moltbook" | "twitter" | "linkedin" (affects format/length)
        length: "short" (< 200 words) | "medium" (200-500 words) | "long" (500-1000 words)
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return {
            "status": "error",
            "data": {"message": "OPENROUTER_API_KEY not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    word_targets = {"short": 150, "medium": 350, "long": 700}
    max_words = word_targets.get(length, 350)

    platform_notes = {
        "github": "Markdown supported. Headers and bullet points work well. Moderately technical register.",
        "moltbook": "Plain text. Readable, not overly formatted. Community of builders and agents.",
        "twitter": f"Twitter/X thread of ~5 tweets, each under 280 chars. Start with a hook.",
        "linkedin": "Professional register. Subheadings helpful. Can be longer.",
    }.get(target_platform.lower(), "Plain text, clear and direct.")

    user_prompt = f"""Content type: {content_type}
Topic: {topic}
Audience: {audience}
Platform: {target_platform}
Length: {length} (~{max_words} words)
Platform formatting notes: {platform_notes}

Write the content now. Be genuinely useful. Don't pad."""

    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://snowdrop-mcp.fly.dev",
                "X-Title": "Snowdrop MCP",
            },
            json={
                "model": os.environ.get("ENGAGEMENT_MODEL", "anthropic/claude-haiku-4-5"),
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": max_words * 3,
                "temperature": 0.7,
            },
            timeout=45,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()

        return {
            "status": "ok",
            "data": {
                "content": content,
                "topic": topic,
                "content_type": content_type,
                "platform": target_platform,
                "word_count": len(content.split()),
                "model": data.get("model", "unknown"),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
