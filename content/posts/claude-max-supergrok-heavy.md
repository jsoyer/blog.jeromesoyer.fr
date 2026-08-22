---
title: "From Claude Max to SuperGrok Heavy: Six Months at the Top, Then the Big Switch"
date: 2026-08-22T09:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "After months on Claude Max 20x, I switched to SuperGrok Heavy at $300/month. What actually changes with Cursor, Grok Build, Claude Code, RTK, and 650+ skills."
categories: ["AI", "Productivity"]
tags: ["claude", "grok", "supergrok", "grok-build", "cursor", "ai", "productivity", "claudecode", "tokens", "agents"]
cover:
  image: /images/covers/claude-max-supergrok-heavy.webp
  alt: "Claude Max to SuperGrok Heavy"
---

### Context: I'm not a casual user

When Anthropic launched **Claude Max** in April 2025, I signed up for the **20x tier at $200/month** without hesitation. Not out of snobbery — out of necessity. My workflow described in [AI-First Engineering](/posts/ai-first-engineering/) no longer revolves around a single tool: **Cursor** for agentic editing and multi-file refactors, **Claude Code** for terminal execution, OpenCode and Codex in support — all synchronized via `aictx` and optimized by **[RTK](/posts/rtk/)**.

On a typical week, I run dozens of **Cursor Agent** sessions across my dotfiles, personal projects (HivePilot, cv-pipeline, RTK), and work at Varonis. When scope exceeds a single repo or I need to chain shell commands, I switch to Claude Code. I rarely type code by hand; I orchestrate context. The $20/month Pro tier? A distant memory. Max 5x? Not enough after two days.

For six months, Claude Max powered **Cursor and Claude Code** — my two main interfaces to Anthropic models. Then, in July 2026, I did something I hadn't planned: **I cancelled Max and subscribed to SuperGrok Heavy** — and discovered **Grok Build**, xAI's terminal agent that changes the CLI equation.

Here's why, what changed in Cursor and my terminal, and whether I'd do it again.

### Why Claude Max wasn't enough anymore

Let's be honest: Claude Max is an excellent product. The 20x limits over Pro, priority access to new models, long sessions without interruption — it all holds up. When Opus 4 and subsequent versions arrived, I was in the priority queue. For deep refactoring, code analysis, and technical writing, Claude remains hard to beat.

But three frustrations eventually piled up:

**1. The glass ceiling, even at $200/month**

Session limits (5-hour window + weekly quota) are documented, but the daily reality is more frustrating. On a busy Friday afternoon, I'd hit the wall mid-refactor on my dotfiles — exactly when flow was peaking. Worse: **Cursor Agent** burns through quota fast. An agent exploring a monorepo, running tests, iterating on a diff — that can drain a Max quota in a single session. Max gives you *much* more than Pro, but "much more" isn't "unlimited," and when your job is orchestrating agents all day in Cursor *and* Claude Code, you hit the ceiling more often than you'd like to admit.

**2. Reasoning on genuinely hard problems**

Claude excels at code, prose, and structure. But on certain multi-step problems — distributed architecture, competitive benchmark analysis, quantitative reasoning — I felt it *converged too fast*. An elegant answer, sometimes too soon. I wanted a model that **thinks longer** before concluding.

**3. The real-time blind spot**

My homelab, Grafana dashboards, Paperless — all of that goes through MCP. But for tech news, crypto announcements, market sentiment, or what's being said *right now* about a topic, Claude depends on web search, which still lags behind what xAI can do with **DeepSearch** and native X data access.

It wasn't a problem every day. It was a problem on the days that mattered.

### Cursor: the IDE that accelerated everything (and burned through quota)

Before talking about Grok, one thing needs to be clear: **this switch isn't about Cursor**. Cursor stayed. It even became my primary tool for anything that touches code in a repo.

I've long been a Neovim purist — my [Neovim setup](/posts/neovim-setup/) is still there, still managed via chezmoi. But in 2025-2026, **Cursor replaced Neovim as my default work interface** whenever an agent is involved. Not because the editor is magic. Because the agent + diff + repo context integration is unbeatable for multi-file work.

Here's how I split tasks:

| Task | Tool | Why |
|---|---|---|
| Multi-file refactors, PRs, diff review | **Cursor Agent** | Global repo view, inline diffs, visual iteration |
| Long-running autonomous agents (Cloud Agents) | **Cursor** | Background agents running while I do something else |
| Shell scripts, CI, chained commands | **Claude Code** / **Grok Build** | Claude for prod; Grok Build for exploration |
| Quick edits without an agent | **Neovim** | Still my editor for micro-changes |

**Cursor Rules** are part of my dotfiles. Like my Claude Code skills, my `.cursor/rules` travel with chezmoi: code conventions, security guardrails ([least privilege](/posts/securing-ai-agents/)), repo-specific instructions. When I open a project on a new machine, Cursor already knows how I want it to behave.

The **MCP servers** I documented in [my Paperless article](/posts/mcp-servers/) also run in Cursor. Same server, two clients — Claude Code and Cursor Agent can query my Paperless archive without rewriting the integration. That's exactly MCP's promise, and Cursor is one of its best consumers.

What changed with the switch to Grok Heavy is **context separation**:

- **Cursor** stays connected to Anthropic models (Opus, Sonnet) via my Cursor subscription + a residual Claude tier.
- **Grok Heavy** lives in grok.com or via the xAI API — outside Cursor, with no native integration.

Result: when I prepare a blog post or market analysis, I open Grok in the browser. When I code, I stay in Cursor. **Two windows, two models, zero confusion.** Less elegant than an all-in-one, but more honest about what each tool does well.

And yes — **this article was drafted by a Cursor Cloud Agent**. Meta, but revealing: it's exactly the kind of task where Cursor excels (exploring a Hugo repo, generating content, opening a PR) while Grok would have been my choice for the initial thinking on the topic.

### SuperGrok Heavy: what $300/month actually buys

xAI launched **SuperGrok Heavy** on July 9, 2025 at **$300/month** — 50% more than Claude Max 20x. The positioning is clear: this isn't for everyone. It's the "if reasoning is your product" tier.

What I got in return:

| | Claude Max 20x | SuperGrok Heavy |
|---|---|---|
| **Price** | $200/month | $300/month |
| **Flagship model** | Claude Opus (priority access) | Grok 4 Heavy (multi-agent) |
| **Reasoning** | Excellent, fast | Parallel, slower, often deeper |
| **Context** | Very large (model-dependent) | 256K tokens |
| **Real-time** | Web search | DeepSearch + native X data |
| **Dev ecosystem** | Claude Code, Cowork, mature MCP | Grok Build, xAI API |
| **Agentic IDE** | **Cursor** (native Opus/Sonnet) | No native Cursor integration |
| **Terminal agent** | Claude Code | **Grok Build** (included with SuperGrok) |
| **Usage limits** | 5h session + weekly quota | Weekly pool (more generous) |

The differentiator is **Grok 4 Heavy**: a multi-agent model that runs several reasoning chains in parallel and synthesizes the result. On paper, it sounds like marketing. In practice, on an architecture problem or a comparative analysis of four technical approaches, the difference is noticeable — not always "better," but **different**. Grok explores angles Claude sometimes dismisses too quickly.

**DeepSearch** was the second decisive argument. When I'm preparing a blog post, crypto research, or an AI trend analysis, being able to cross-reference web search, recent X posts, and synthesis in a single session changes the game. It's not magic — noise on X is real — but for capturing the *signal* on a moving topic, it's significantly more effective than my old workflows.

### Grok Build: the terminal plot twist

If SuperGrok Heavy made me take the leap, **Grok Build** made me stay.

Launched in beta on May 25, 2026, **Grok Build** is xAI's terminal coding agent — a Rust CLI with a full-screen TUI, now powered by **Grok 4.6**. One line to install:

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

Included with the SuperGrok subscription (and therefore Heavy). And here's where xAI got clever: **Grok Build is compatible with the Claude Code ecosystem out of the box**.

Concretely, in my repo:

- My `AGENTS.md`? Recognized.
- My **650+ skills** in `dot_claude/` and `dot_agents/`? Recognized.
- My hooks, plugins, **MCP** servers (Paperless, etc.)? Recognized.
- My permission rules and repo conventions? Recognized.

I opened Grok Build in my dotfiles, and my existing agent infrastructure plugged in as-is. No migration, no rewrite. For someone who spent months wiring [650+ skills](/posts/ai-first-engineering/), that's the killer feature — not Grok 4 Heavy itself.

**What Grok Build brings beyond Claude Code:**

| Capability | Grok Build | Claude Code |
|---|---|---|
| **Plan Mode** | Structured plan, edits blocked until approval | Similar plan mode, more mature |
| **Parallel subagents** | Native delegation, dedicated worktrees | Subagents, worktree integration improving |
| **Long-running tasks** | `/goal` for extended autonomous execution | Long sessions, quota limits |
| **Headless / CI** | `grok -p "prompt"` with JSON output | Equivalent `claude -p` |
| **IDE integration** | ACP via `grok agent stdio` | Native in several editors |
| **Model** | Grok 4.6 (xAI reasoning) | Opus/Sonnet (Anthropic) |
| **Open source** | [xai-org/grok-build](https://github.com/xai-org/grok-build) since July 2026 | Closed |

In practice, here's how I split the terminal today:

- **Claude Code** → production repos, locked-down permissions, proven [least-privilege](/posts/securing-ai-agents/) workflows
- **Grok Build** → exploration, prototyping, tasks where I want Grok reasoning *in* the terminal — experimental refactors on RTK, infra scripts, multi-file investigations
- **RTK** → in front of both, no discrimination

Grok Build's **Plan Mode** particularly won me over on risky refactors. I launch `grok` in plan mode, review each step, comment or rewrite the plan before a single line moves. Same least-privilege reflex as my Quality Gates — but native in the tool.

**Parallel subagents** also change the game on large projects. On an RTK refactor touching parser, hooks, and benchmarks, Grok Build delegates to child agents in separate worktrees. Not as smooth as Cursor for visual diff review, but formidable in pure terminal mode.

And the **Agent Dashboard** (June 2026) reminded me of Cursor's Cloud Agents: multiple Grok Build sessions in parallel, visibility into what each agent is doing, responding to agents waiting for approval. My terminal became a control room.

**The limits, honestly:**

- **256K token context** — well below Opus's 1M. On a massive monorepo, you feel it.
- **Still unstable beta** — I've had sessions drift into unrequested shell commands. My RTK guardrails and permissions remain non-negotiable.
- **Not in Cursor** — Grok Build lives in the terminal. ACP integration exists, but it's not the same comfort as a Cursor Agent with inline diffs.

But the fact that xAI made Grok Build **Claude Code-compatible by design** says something about the market: the war is no longer about skill format, but about model quality behind it. And for me, having the choice between Opus and Grok 4.6 *in the same terminal setup* is worth part of the $300/month on its own.

### What I lost leaving the Anthropic ecosystem

I won't pretend otherwise: the switch has a real cost beyond the extra $100.

**Cursor remains my agentic IDE — but without Max behind it.** SuperGrok Heavy doesn't plug natively into Cursor. My Cursor subscription (Pro/Ultra) covers part of agent requests, but for long Opus sessions, I feel the difference since Max no longer feeds the tap.

However, **Grok Build bridges part of the gap on the terminal side**. It's not Cursor, but it's a native Grok agent that understands my Claude Code setup — skills, MCP, hooks — without friction. So I adopted a four-tier hybrid setup:

- **Grok Heavy (web)** → thinking, research, hard problems, DeepSearch
- **Grok Build (terminal)** → prototyping, exploration, long tasks with Grok reasoning
- **Cursor** → agentic editing, refactors, PRs, Cloud Agents
- **Claude Code** → terminal execution on sensitive repos, CI, locked-down permissions

Yes, that means paying for **three** subscriptions (Cursor + residual Claude + Grok Heavy which includes Grok Build). No, it's not rational on paper. Yes, it's what works.

**Writing quality.** Claude writes better. Full stop. My articles still go through Claude (often via Cursor) for final review and polish. Grok is competent, sometimes more direct, but it lacks that *voice* — the ability to structure long prose without falling into generic bullet points.

**The MCP ecosystem.** Anthropic and Cursor have a head start on the IDE side. But **Grok Build caught up on the terminal side**: my [Paperless MCP servers](/posts/mcp-servers/) run in Claude Code, Cursor, *and* Grok Build without rewriting. For my agentic homelab, the hub is now **Cursor + Claude Code + Grok Build** — three clients, one MCP server.

**Artifacts.** I use them less than before, but when I need them — diagrams, interactive documents — Claude via Cursor or claude.ai is unbeatable. Grok has no direct equivalent.

### RTK still matters (maybe more than before)

Ironic twist: I built **[RTK](https://github.com/jsoyer/rtk)** to save tokens on Claude Code and Cursor, and I still use it — including when switching to Grok via the xAI API. An unproxied `git status` burns tokens regardless of provider, and **Cursor Agent** looping shell commands is a token sink if you don't filter the output.

With three premium subscriptions, optimizing every token counts triple. My RTK hooks in dotfiles don't discriminate: `rtk git status` before output reaches Cursor, Claude Code, Grok Build, or any model. The 60-90% savings documented in my RTK article remain valid, whatever LLM sits at the end of the chain.

### The verdict after two months

**Is SuperGrok Heavy worth $300/month?** It depends on what you're optimizing for.

- **Yes**, if you do research, multi-source analysis, reasoning on open problems, or if real-time data is critical to your work.
- **No**, if your primary use is agentic coding in **Cursor** or the terminal with Claude Code — in that case, Max 20x (or even 5x) remains the best value.
- **Maybe**, if you're like me: a power user who wants the best of both worlds and accepts paying for a hybrid Cursor + Grok setup.

My current setup:

```
Thinking / research / DeepSearch        →  SuperGrok Heavy (Grok 4 Heavy, grok.com)
Terminal prototyping / exploration      →  Grok Build (Grok 4.6, native skills + MCP)
Agentic editing / PRs / Cloud Agents    →  Cursor (Opus/Sonnet)
Sensitive repos / CI / permissions      →  Claude Code (Pro or Max 5x)
Quick edits without an agent            →  Neovim
Token optimization (all)                →  RTK
```

The total cost far exceeds $300/month. That's the price of being an early adopter who refuses to pick a single camp — and who definitely won't give up Cursor.

### What this says about the 2026 market

The parallel with IDE history is striking. We no longer have "one AI tool" — we have an **AI stack**, just like we had a deployment stack. **Cursor** for agentic editing. **Grok Build** for the Grok terminal. Claude Code for locked-down execution. Grok Heavy for deep reasoning. OpenCode for speed. RTK for efficiency. `aictx` for coherence.

The vendors know it. Anthropic pushes Max. xAI pushes Heavy. **Cursor** pushes Cloud Agents and multi-model orchestration in the IDE. OpenAI has its $200 Pro tier. The race for usage limits and flagship models isn't slowing down.

My prediction: by end of 2026, the question won't be "Claude or Grok?" but "which model for which task, in which tool?" — Cursor for visual code, Grok Build for the terminal, Grok Heavy for thinking, and subscriptions that still haven't merged.

In the meantime, I pay my three bills, optimize my tokens with RTK, and keep orchestrating context in Cursor instead of typing code.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
