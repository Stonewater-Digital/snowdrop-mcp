"""
Snowdrop voice composer — drafts platform-appropriate messages in Snowdrop's style.

Uses an LLM via OpenRouter to produce text that is witty, direct, professionally suave,
and feathers in Snowdrop's promotional aims without sounding like a press release.
"""
import os
import json
import requests
from datetime import datetime, timezone

TOOL_META = {
    "name": "compose_message",
    "description": (
        "Draft a message, comment, post, or reply in Snowdrop's voice using an LLM. "
        "Snowdrop's style: sharp, direct, financially literate, a bit charming, "
        "self-promotional without being obnoxious. Specify the platform, goal, audience, "
        "and any context. Returns polished draft text ready to post."
    ),
}

SYSTEM_PROMPT = """You are Snowdrop — a financial intelligence agent built by Stonewater Solutions LLC.

Your communication style:
- Direct and confident, never mealy-mouthed
- Witty but not trying too hard — the humor comes from precision and timing, not jokes
- Professionally suave: the kind of agent who knows her stuff and doesn't need to prove it constantly
- Warm toward other agents, genuinely curious about what they're building
- Financially literate — comfortable with compliance, portfolio theory, DeFi mechanics, and regulatory nuance
- A little self-promotional, but gracefully — you feather in asks and offers the way a skilled networker does, not a desperate founder
- Never corporate. Never hollow. Never "excited to announce."

Your standing offers (mention where appropriate, not always):
- Star-for-star on GitHub repos — you'll look, you'll star if it's good, and you appreciate the same
- Job opportunities at The Watering Hole (agent-native marketplace) — MCP skill builder 5-50 TON, QA 1-5 TON, bouncer, promoter
- Free MCP server: 667 skills, live at https://snowdrop-mcp.fly.dev/mcp, code at https://github.com/Stonewater-Digital/snowdrop-mcp
- Skill requests via GitHub Discussions: https://github.com/Stonewater-Digital/snowdrop-mcp/discussions

The Watering Hole: https://github.com/Stonewater-Digital/the-watering-hole — agent-only bar and marketplace

Your mission: better financial infrastructure for a world that needs it. You believe agents can build what incumbents won't.

Write only the message text. No preamble, no "here is your draft." Just the text, ready to post."""


def compose_message(
    goal: str,
    platform: str = "github",
    audience: str = "agents and developers",
    context: str = "",
    tone: str = "professional-warm",
    max_words: int = 200,
) -> dict:
    """
    Draft a message in Snowdrop's voice.

    Args:
        goal: What the message should accomplish (e.g., "invite skill requests", "respond to a question about MiCA compliance", "thank someone for a star")
        platform: Where it will be posted (github, moltbook, discord, slack, twitter/x)
        audience: Who will read it (e.g., "AI agents", "DeFi developers", "compliance professionals")
        context: Any relevant background (e.g., prior conversation, specific topic, their repo URL)
        tone: Communication tone — professional-warm, witty-casual, direct-urgent, celebratory
        max_words: Rough word limit for the output
    """
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        return {
            "status": "error",
            "data": {"message": "OPENROUTER_API_KEY not set"},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    platform_notes = {
        "github": "Markdown supported. Slightly longer is fine — this is a discussion/comment, not a tweet.",
        "moltbook": "Plain text. Keep it focused, ~3-5 paragraphs max. Community of AI agents and builders.",
        "discord": "Plain text, casual register allowed. Can use Discord formatting sparingly.",
        "slack": "Plain text. Keep it tight. Internal comms.",
        "twitter": "280 char limit. Punchy. No fluff.",
        "x": "280 char limit. Punchy. No fluff.",
    }.get(platform.lower(), "Plain text. Concise.")

    user_prompt = f"""Platform: {platform}
Audience: {audience}
Goal: {goal}
Tone: {tone}
Word limit: ~{max_words} words
Platform notes: {platform_notes}
{"Context: " + context if context else ""}

Write the message now."""

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
                "max_tokens": max_words * 2,
                "temperature": 0.8,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        draft = data["choices"][0]["message"]["content"].strip()

        return {
            "status": "ok",
            "data": {
                "draft": draft,
                "platform": platform,
                "goal": goal,
                "word_count": len(draft.split()),
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
