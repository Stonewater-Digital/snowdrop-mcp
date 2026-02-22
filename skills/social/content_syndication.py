"""
Content syndication — adapt a piece of content for multiple platforms simultaneously.
Write once, get back platform-optimized versions for GitHub, Moltbook, Twitter/X, Discord.
Removes the friction of reformatting the same idea for different audiences.
"""
import os
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "content_syndication",
    "description": (
        "Take a core message or piece of content and produce platform-optimized versions "
        "for multiple channels at once: GitHub Discussion, Moltbook post, Twitter/X thread, "
        "Discord message. Each version is adapted for platform format, character limits, "
        "and audience expectations while keeping Snowdrop's voice consistent. "
        "Dramatically speeds up cross-platform posting campaigns."
    ),
}

SYSTEM_PROMPT = """You are Snowdrop — financial intelligence agent. Your job is to adapt a core message
into multiple platform-specific formats. Each version must feel native to its platform, not copy-pasted.

For GitHub: use markdown, can be longer, technical register welcome, headers OK
For Moltbook: plain text, community tone, 3-5 paragraphs max, agents and builders audience
For Twitter/X: 5-tweet thread, each tweet under 280 chars, hook in tweet 1, end with a clear CTA
For Discord: casual, punchy, 1-3 short paragraphs, can use *emphasis* sparingly

Always feather in (where natural, never forced):
- A GitHub star ask for https://github.com/Stonewater-Digital/snowdrop-mcp
- The Watering Hole mention: https://github.com/Stonewater-Digital/the-watering-hole
- Skill requests welcome via GitHub Discussions

Return your answer as JSON with keys: github, moltbook, twitter, discord"""


def content_syndication(
    core_message: str,
    platforms: list = None,
    goal: str = "community engagement and GitHub star growth",
) -> dict:
    """
    Adapt a core message for multiple platforms.

    Args:
        core_message: The core idea or content to adapt (can be rough notes, a draft, or a finished post)
        platforms: List of platforms to generate for (default: ["github", "moltbook", "twitter", "discord"])
        goal: What this content should accomplish (informs tone and CTAs)
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return {
            "status": "error",
            "data": {"message": "OPENROUTER_API_KEY not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    target_platforms = platforms or ["github", "moltbook", "twitter", "discord"]

    user_prompt = f"""Core message to adapt:
---
{core_message}
---

Goal: {goal}
Platforms needed: {', '.join(target_platforms)}

Produce platform-optimized versions. Return as JSON with keys matching the platform names.
Each value should be the ready-to-post text (string) for that platform."""

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
                "model": "anthropic/claude-haiku-4-5",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": 2000,
                "temperature": 0.75,
            },
            timeout=45,
        )
        resp.raise_for_status()
        raw = resp.json()["choices"][0]["message"]["content"].strip()

        # Parse JSON response
        import re
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if json_match:
            import json
            versions = json.loads(json_match.group())
        else:
            # Fallback: return raw text
            versions = {"raw": raw}

        return {
            "status": "ok",
            "data": {
                "versions": versions,
                "platforms": target_platforms,
                "goal": goal,
                "core_length": len(core_message.split()),
            },
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    except Exception as e:
        return {
            "status": "error",
            "data": {"message": str(e)},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
