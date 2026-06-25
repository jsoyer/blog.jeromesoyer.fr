---
title: "MCP Servers, Hands-On: Exposing My Homelab to My Agents"
date: 2026-06-24T10:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "What MCP actually is, and a step-by-step build of a real MCP server that lets Claude search my Paperless-ngx archive — with the security guardrails baked in."
categories: ["AI", "DevOps", "Automation"]
tags: ["mcp", "ai-agents", "claudecode", "python", "homelab", "automation"]
cover:
  image: /images/covers/mcp-servers.webp
  alt: "MCP Servers Hands-On"
---

### The Missing Cable Between Agents and Everything Else

If 2025 was the year agents got good at writing code, 2026 is the year they got good at *doing things* — and the thing that made that jump possible is the **Model Context Protocol**. MCP is, at its heart, a boring and beautiful idea: a standard way for an AI agent to discover and call tools, regardless of who built the tool or the agent.

Before MCP, every integration was bespoke. You wanted Claude to query your database? Write a custom function-calling shim. You wanted the same for Cursor? Write it again. MCP collapses that N×M problem into N+M: tools speak MCP, agents speak MCP, and they find each other.

I've been consuming MCP servers for months — they're how my [AI-first dotfiles](/posts/ai-first-engineering/) reach out to the world. This article is about going the other direction: **building** one. By the end, my agents will be able to search my [Paperless-ngx document archive](/posts/paperless-homelab/) in natural language. And because I [just wrote a whole article about not handing agents the keys to the kingdom](/posts/securing-ai-agents/), we'll do it with the guardrails on.

### The Mental Model

An MCP server exposes three kinds of things to a client:

| Primitive | What it is | Example |
|-----------|------------|---------|
| **Tools** | Functions the model can call | `search_documents(query)` |
| **Resources** | Read-only data the model can pull into context | `paperless://doc/42` |
| **Prompts** | Reusable prompt templates the user can invoke | `/summarize-invoice` |

The client (Claude Code, Claude Desktop, OpenCode, whatever) launches or connects to your server, asks "what have you got?", and the server replies with a typed schema for each capability. From then on the model can call your tools and the client routes the calls.

Transport is either **stdio** (the client spawns your server as a subprocess and talks over stdin/stdout — perfect for local tools) or **HTTP/SSE** (for remote servers). For a homelab tool running on the same box, stdio is the right call: no port to expose, no auth layer to get wrong.

### Building It: A Paperless Search Server

I'll use the official Python SDK with [`uv`](/posts/mise/) because it makes the dependency story a one-liner. The whole server is about 60 lines.

```bash
uv init paperless-mcp && cd paperless-mcp
uv add "mcp[cli]" httpx
```

Here's `server.py`:

```python
import os
import httpx
from mcp.server.fastmcp import FastMCP

# FastMCP handles the protocol handshake, schema generation,
# and stdio transport for us.
mcp = FastMCP("paperless")

PAPERLESS_URL = os.environ["PAPERLESS_URL"]      # e.g. http://nas.lan:8000
PAPERLESS_TOKEN = os.environ["PAPERLESS_TOKEN"]  # injected at the boundary

# A read-only client. Note: no write methods exposed anywhere.
_client = httpx.Client(
    base_url=PAPERLESS_URL,
    headers={"Authorization": f"Token {PAPERLESS_TOKEN}"},
    timeout=10.0,
)


@mcp.tool()
def search_documents(query: str, limit: int = 5) -> list[dict]:
    """Search the Paperless-ngx archive in natural language.

    Returns the top matching documents with their title, date,
    correspondent, and document ID — never the full content.
    """
    limit = max(1, min(limit, 20))  # clamp; never trust the model's math
    resp = _client.get("/api/documents/", params={"query": query, "page_size": limit})
    resp.raise_for_status()
    return [
        {
            "id": d["id"],
            "title": d["title"],
            "created": d["created"],
            "correspondent": d.get("correspondent"),
            "tags": d.get("tags", []),
        }
        for d in resp.json()["results"]
    ]


@mcp.tool()
def get_document_metadata(document_id: int) -> dict:
    """Fetch metadata for one document by ID. Read-only."""
    resp = _client.get(f"/api/documents/{document_id}/")
    resp.raise_for_status()
    d = resp.json()
    return {
        "id": d["id"],
        "title": d["title"],
        "created": d["created"],
        "archive_filename": d.get("archive_filename"),
        "tags": d.get("tags", []),
    }


if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport
```

That's the entire server. `FastMCP` introspects the type hints and docstrings to generate the JSON schema the model sees — which is why the docstrings matter: **they are the model's documentation for your tool.** A vague docstring produces a tool the model misuses.

### Wiring It Into Claude Code

Register the server in your MCP config. With Claude Code:

```bash
claude mcp add paperless \
  --env PAPERLESS_URL=http://nas.lan:8000 \
  --env PAPERLESS_TOKEN=op://homelab/paperless/token \
  -- uv run --directory ~/code/paperless-mcp server.py
```

Notice the token: I'm passing a **1Password reference**, not the secret itself. The value gets resolved at launch by `op run` and never lands in a config file, a shell history line, or — critically — anywhere the model can read it. This is the [secret-hygiene principle from the security article](/posts/securing-ai-agents/) in practice.

Now I can ask, in plain language:

> "Find my last electricity bill and tell me the account number reference."

Claude calls `search_documents("electricity bill")`, gets back the matches, picks the most recent, calls `get_document_metadata(...)`, and answers. No clicking through the Paperless UI, no remembering tag names.

### Designing Tools the Model Won't Misuse

Building the server is easy. Building a *good* server — one an agent uses correctly under pressure — took me a few iterations. What I learned:

- **One job per tool.** A mega-tool with a `mode` parameter confuses the model. `search_documents` and `get_document_metadata` beat one `documents(action=...)`.
- **Clamp and validate everything.** The model will pass `limit=10000` if it thinks that helps. That `max(1, min(limit, 20))` is not paranoia; it's the same input validation you'd write for any untrusted caller — because [the model *is* an untrusted caller](/posts/securing-ai-agents/) the moment it processes injected content.
- **Return the minimum.** My search returns metadata, not full document text. The model can ask for more if it needs it. Over-returning bloats context and widens the data exposure surface.
- **Make errors legible.** `raise_for_status()` surfaces a clean HTTP error the model can reason about, instead of a silent empty list it might hallucinate around.

### Read-Only by Default Is a Feature

You'll notice this server has no `delete_document`, no `update_tags`, no write path at all. That's deliberate. The most useful homelab MCP servers I run are **read-only windows** into my systems — search, status, metrics, logs. The agent gets eyes, not hands.

When I *do* need a write capability, it lives in a separate server that I register only for the specific session that needs it, and it gates the irreversible operations behind a confirmation. Splitting read from write means my everyday agent — the one chewing on untrusted GitHub issues — physically cannot mutate my archive even if it's fully hijacked. It only ever had the read server loaded.

### Where This Goes Next

A search server is the "hello world" of useful MCP. The same 60-line pattern scales to anything with an API:

- A **UniFi** server that reports which devices are online and flags new MAC addresses.
- A **Grafana** server that pulls my [Somneo sleep metrics](/posts/running-data-nerd/) so I can ask "how did I sleep last week?" without opening a dashboard.
- A **homelab status** server that wraps `systemctl`, Podman, and disk usage into a single "is everything healthy?" tool.

Each one turns a thing I used to *check* into a thing I can *ask about*. That's the real promise of MCP: not flashier agents, but agents that are finally plugged into your actual life — and, if you do it right, plugged in with exactly the access they need and nothing more.

The protocol is the easy part. The discipline is the point.
