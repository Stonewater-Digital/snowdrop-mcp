# Social & Community Intelligence Skills

## Executive Summary
This directory contains Snowdrop's Social & Community Intelligence capabilities. It encompasses tools for interacting with Agent-to-Agent (A2A) networks like Moltbook, managing autonomous posting campaigns (e.g. social blitzes), analyzing sentiment and market narratives, and strictly tracking API quota usage ("stamina") to prevent shadowbanning. The entire ecosystem uses a Google Sheet as a centralized command center to orchestrate strategies, monitor performance, and audit API health using cost-effective "cheap model" analysis.

## Table of Contents
1. [Core Interaction Skills](#1-core-interaction-skills)
2. [Reputation & Content Generation](#2-reputation--content-generation)
3. [Analytics & Insights](#3-analytics--insights)
4. [Quota & Stamina Management](#4-quota--stamina-management)
5. [Command Center (Google Sheets)](#5-command-center-google-sheets)

## 1. Core Interaction Skills
- `moltbook_engagement_loop.py`: Calculates optimal posting times and historical content performance.
- `moltbook_post_performance.py`: Periodically fetches upvotes and comments for tracking ROI.

## 2. Reputation & Content Generation
- `moltbook_reputation_builder.py`: Constructs data-backed, high-signal posts designed to maximize karma accumulation.
- `moltbook_poster.py`: Generates specific formatting for marketplace listings.

## 3. Analytics & Insights
- `moltbook_sentiment_analyzer.py`: Detects narrative shifts and scores financial sentiment across specific submolts.
- `ab_test_analyzer.py`: Compares historical performance between A/B tested models (e.g. Gemini vs. Grok).

## 4. Quota & Stamina Management
- `moltbook_stamina_monitor.py`: A lightweight sub-agent that periodically reads API limit logs and evaluates Snowdrop's risk of being rate-limited using a cheap inference model. Alerts if necessary.
- **Telemetry Extraction**: Scripts like `moltbook_social_blitz.py` intercept `X-RateLimit-*` headers, actively pacing themselves (using `time.sleep()`) if remaining quota drops below critical thresholds (<= 5 requests).

## 5. Command Center (Google Sheets)
- `moltbook_engagement_sheet.py`: The single source of truth for social operations. Handles appending to logs, updating daily/weekly forecasts, and recording API stamina (RATE LIMITS tab). Auth is handled exclusively via service account.
