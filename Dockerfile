# syntax=docker/dockerfile:1
# Snowdrop MCP Community Edition — self-hostable MCP server
#
# Build: docker build -t snowdrop-community .
# Run:   docker run -p 8000:8000 snowdrop-community
#
# Security notes:
#   - Runs as non-root user 'snowdrop'
#   - No secrets, no auth — this is the free community edition

FROM python:3.11-slim AS base

# Non-root user
RUN groupadd -r snowdrop && useradd -r -g snowdrop snowdrop

WORKDIR /app

# Emit stdout/stderr immediately
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Dependencies (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

# Application source
COPY --chown=snowdrop:snowdrop . .

# Runtime
USER snowdrop

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8000}/health')" \
    || exit 1

CMD ["python", "mcp_server.py"]
