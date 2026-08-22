---
title: "From Claude Max to SuperGrok Heavy: Six Months at the Top, Then the Big Switch"
date: 2026-08-22T09:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "After months on Claude Max 20x, I switched to SuperGrok Heavy at $300/month. Herdr, Moshi, Grok Build CLI — and the Claude mobile app I'll already miss."
categories: ["AI", "Productivity"]
tags: ["claude", "grok", "supergrok", "grok-build", "herdr", "moshi", "ai", "productivity", "claudecode", "tokens", "agents"]
cover:
  image: /images/covers/claude-max-supergrok-heavy.webp
  alt: "Claude Max to SuperGrok Heavy"
---

### Context: I'm not a casual user

When Anthropic launched **Claude Max** in April 2025, I signed up for the **20x tier at $200/month** without hesitation. Not out of snobbery — out of necessity. My workflow described in [AI-First Engineering](/posts/ai-first-engineering/) never revolved around a graphical IDE: it's **the CLI, always the CLI**. **Claude Code** and **Grok Build** in **Herdr** panes, steered from the couch via **Moshi** on iPhone, synchronized via `aictx` and optimized by **[RTK](/posts/rtk/)**.

I have a Cursor subscription on a small plan. I barely use it. Not out of principle — out of habit. My brain lives in Kitty, my agents live in Herdr, and my phone is a remote control via Moshi. I rarely type code by hand; I orchestrate context. The $20/month Pro tier? A distant memory. Max 5x? Not enough after two days.

For six months, Claude Max powered **Claude Code, the Claude mobile app, and my Herdr sessions**. Then, in July 2026, I did something I hadn't planned: **I cancelled Max and subscribed to SuperGrok Heavy** — and discovered **Grok Build**, xAI's terminal agent that slots into the same Herdr setup without breaking anything.

Here's why, what changed in my terminal, and what I already regret.

### Why Claude Max wasn't enough anymore

Let's be honest: Claude Max is an excellent product. The 20x limits over Pro, priority access to new models, long sessions without interruption — it all holds up. When Opus 4 and subsequent versions arrived, I was in the priority queue. For deep refactoring, code analysis, and technical writing, Claude remains hard to beat.

But three frustrations eventually piled up:

**1. The glass ceiling, even at $200/month**

Session limits (5-hour window + weekly quota) are documented, but the daily reality is more frustrating. On a busy Friday afternoon, I'd hit the wall mid-refactor on my dotfiles — exactly when flow was peaking. Worse: a **Herdr** session with three parallel Claude Code agents burns through quota fast. An agent exploring a monorepo, running tests, iterating on a diff — that can drain a Max quota in a single session. Max gives you *much* more than Pro, but "much more" isn't "unlimited," and when your job is orchestrating agents all day in Herdr, you hit the ceiling more often than you'd like to admit.

**2. Reasoning on genuinely hard problems**

Claude excels at code, prose, and structure. But on certain multi-step problems — distributed architecture, competitive benchmark analysis, quantitative reasoning — I felt it *converged too fast*. An elegant answer, sometimes too soon. I wanted a model that **thinks longer** before concluding.

**3. The real-time blind spot**

My homelab, Grafana dashboards, Paperless — all of that goes through MCP. But for tech news, crypto announcements, market sentiment, or what's being said *right now* about a topic, Claude depends on web search, which still lags behind what xAI can do with **DeepSearch** and native X data access.

It wasn't a problem every day. It was a problem on the days that mattered.

### Herdr + Moshi: my actual workflow (not Cursor)

Let's be clear: **I'm not a Cursor user**. I have a small subscription, I tried it, and I went back to the terminal. That's not a criticism of Cursor — the tool is excellent for people who live in a graphical IDE. It's just not *my* workflow.

My setup since early 2026 is **Herdr + Moshi**:

**[Herdr](https://herdr.dev)** is a native terminal multiplexer for AI agents — think "tmux, but it knows a pane is running Claude Code and whether it's `working`, `blocked`, or `done`." My agents run in persistent Herdr panes on my MacBook or homelab. I close the lid, I disconnect SSH, the agents keep going. I reopen Herdr, everything's still there.

**[Moshi](https://getmoshi.app)** is the mobile complement: an iOS terminal built to steer agents remotely over SSH/Mosh. With `moshi-hook` installed on the host, I get push notifications when an agent needs approval, a unified inbox for Claude Code and Grok Build, and on-device dictation to send prompts from the couch. Herdr and Moshi are made for each other — Moshi detects Herdr workspaces and exposes a dedicated shortcut panel.

Here's how I actually split tasks:

| Task | Tool | Why |
|---|---|---|
| Parallel agents, long sessions | **Herdr** + Claude Code / Grok Build | Persistent panes, visible agent state, CLI orchestration |
| Mobile steering, approvals | **Moshi** + `moshi-hook` | Notifications, inbox, Mosh that survives network drops |
| Sensitive repos, locked permissions | **Claude Code** | Proven [least-privilege](/posts/securing-ai-agents/) workflows |
| Exploration, Grok reasoning | **Grok Build** | Same skills, different model, same Herdr pane |
| Quick edits without an agent | **Neovim** | Still my editor for micro-changes |
| Graphical agentic IDE | **Cursor** | Subscribed, almost never opened |

My **650+ skills**, hooks, plugins, and **MCP** servers (Paperless, etc.) live in my dotfiles and work in Claude Code *and* Grok Build — regardless of which Herdr pane I launch them in. Herdr doesn't wrap agents; it gives them a **persistent runtime**. Moshi doesn't replace the terminal; it gives me a **mobile window** onto that runtime.

Typical evening scenario: I launch three agents in Herdr on my Mac — one on RTK, one on my dotfiles, one on a blog post. I go for a run. My iPhone buzzes via Moshi: the RTK agent is `blocked`, it wants to confirm a `git push`. I approve from the Moshi inbox without reopening the laptop. That's my workflow. No inline diffs in an IDE — pure terminal orchestration.

What changed with the switch to Grok Heavy:

- **Grok Heavy (web/app)** → thinking, DeepSearch, real-time analysis
- **Grok Build** → new Herdr pane, same skills, Grok model
- **Claude Code** → still there for prod and permissions
- **Moshi** → unchanged, but the inbox only half-speaks Claude now

**Three interfaces, two ecosystems, one Herdr multiplexer.**

*(Irony: this article was drafted by a Cursor Cloud Agent — a tool I don't use daily. Proof that the agent market plays out beyond the terminal too, even for CLI purists.)*

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
| **Mobile** | **Claude app** (Max) + Moshi | Grok app (less mature) |
| **Agent multiplexer** | Herdr | Herdr (unchanged) |
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

**Parallel subagents** also change the game on large projects. On an RTK refactor touching parser, hooks, and benchmarks, Grok Build delegates to child agents in separate worktrees. Herdr shows each pane's state in the sidebar — `working`, `blocked`, `done` — without scrolling through three terminals.

And Grok Build's **Agent Dashboard** (June 2026) looks like what Herdr already does natively: multiple parallel sessions, visibility into what each agent is doing, responding to agents waiting for approval. My multiplexer became a control room — except Herdr orchestrates it, not an IDE.

**The limits, honestly:**

- **256K token context** — well below Opus's 1M. On a massive monorepo, you feel it.
- **Still unstable beta** — I've had sessions drift into unrequested shell commands. My RTK guardrails and permissions remain non-negotiable.
- **No Moshi equivalent** — Grok has no `moshi-hook`. I can steer Grok Build from Moshi (it's a real terminal), but not agent-aware notifications, a unified inbox, or lock-screen approvals for Grok like Claude Code gets.

But the fact that xAI made Grok Build **Claude Code-compatible by design** says something about the market: the war is no longer about skill format, but about model quality behind it. And for me, having the choice between Opus and Grok 4.6 *in the same terminal setup* is worth part of the $300/month on its own.

### What I actually miss: the Claude mobile app

The switch to Grok Heavy didn't make me regret Cursor — I wasn't using it anyway. What I *already* miss is **the Claude mobile app**.

With Claude Max, the iOS app was my pocket interface for everything that wasn't code: brainstorming an article, summarizing a PDF, asking a quick question on the go, dictating an idea between meetings. Clean, fast, synced with my Max account. No SSH, no Herdr, no Moshi — just Claude in my pocket.

The Grok app exists. It's improving. But today, it doesn't offer the same fluidity for everyday intellectual work outside the terminal. When I'm on the train and want to sharpen an article angle, I open Grok and... it gets the job done, without the same *presence*. Subjective, but it's the first concrete regret of the switch.

**Moshi fills part of the gap — but not all.** Moshi reconnects me to my Herdr agents from iPhone: approvals, inbox, long sessions. Great for *steering* code remotely. Not the same as a Claude conversation on the couch with no terminal underneath. Two different use cases:

| Need | Claude app (before) | Moshi + Herdr (now) | Grok app (now) |
|---|---|---|---|
| Quick question, writing | ✅ Native, fluid | ❌ Overkill | ⚠️ Fine, less polished |
| Steer a running agent | ❌ | ✅ Inbox, push, approvals | ❌ No equivalent hook |
| Long autonomous session | ⚠️ Limited on mobile | ✅ Agent runs on host | ⚠️ Web/app only |
| Off-network / no laptop | ✅ | ⚠️ Needs host running | ✅ |

Result: I'll probably keep a **minimal Claude Pro tier** just for the mobile app — even though my terminal moved to Grok. Irony: I left Max to save on terminal quota, and I may end up paying Anthropic again for my pocket.

### The rest of what I lost

The switch has other costs beyond the extra $100 and the mobile app.

**Writing quality.** Claude writes better. Full stop. My articles still go through Claude for final review and polish — often from the mobile app or Claude Code in a Herdr pane. Grok is competent, sometimes more direct, but it lacks that *voice*.

**The MCP ecosystem on the terminal side.** **Grok Build caught up**: my [Paperless MCP servers](/posts/mcp-servers/) run in Claude Code and Grok Build without rewriting, in the same Herdr workspace. For my agentic homelab, the hub is **Herdr + Claude Code + Grok Build** — two agents, one multiplexer, one Moshi.

**Artifacts.** I use them less than before, but when I need them — diagrams, interactive documents — Claude via claude.ai or the mobile app is unbeatable. Grok has no direct equivalent.

### RTK still matters (maybe more than before)

Ironic twist: I built **[RTK](https://github.com/jsoyer/rtk)** to save tokens on Claude Code and Grok Build in Herdr, and I still use it. An unproxied `git status` burns tokens regardless of provider, and an agent looping shell commands in a Herdr pane is a token sink if you don't filter the output.

With SuperGrok Heavy + a residual Claude tier for the mobile app, optimizing every token counts double. My RTK hooks in dotfiles don't discriminate: `rtk git status` before output reaches Claude Code, Grok Build, or any model.

### The verdict after two months

**Is SuperGrok Heavy worth $300/month?** It depends on what you're optimizing for.

- **Yes**, if you do research, multi-source analysis, reasoning on open problems, or if real-time data is critical to your work.
- **No**, if your primary use is the terminal with Claude Code — Max 20x (or even 5x) remains the best value.
- **Maybe**, if you're like me: Herdr/Moshi CLI workflow, Grok for thinking, residual Claude for your pocket.

My current setup:

```
Thinking / research / DeepSearch        →  SuperGrok Heavy (Grok 4 Heavy, grok.com)
Terminal exploration / prototyping      →  Grok Build (Herdr pane, native skills + MCP)
Sensitive repos / CI / permissions      →  Claude Code (Herdr pane, residual Pro tier)
Agent orchestration / sessions          →  Herdr (persistent multiplexer)
Mobile steering / approvals             →  Moshi + moshi-hook
Quick off-terminal conversation         →  Claude app (Pro tier — keep it?)
Quick edits without an agent            →  Neovim
Token optimization (all)                →  RTK
```

The total cost far exceeds $300/month — especially if I keep Claude Pro for the mobile app. That's the price of a CLI workflow that refuses to pick a single camp.

### What this says about the 2026 market

The parallel with IDE history is striking — except for me, the IDE is the terminal. We no longer have "one AI tool" — we have an **AI stack**: **Herdr** for orchestration, **Moshi** for mobile, **Grok Build** and **Claude Code** for execution, **Grok Heavy** for thinking, **RTK** for efficiency, `aictx` for coherence.

The vendors know it. Anthropic pushes Max — and a mobile app I already miss. xAI pushes Heavy and Grok Build. Herdr and Moshi fill the gap that neither Cursor nor native apps cover for CLI purists.

My prediction: by end of 2026, the question won't be "Claude or Grok?" but "which model for which surface?" — terminal via Herdr, pocket via the native app or Moshi, thinking via Grok Heavy — and subscriptions that still haven't merged.

In the meantime, I pay my bills, optimize my tokens with RTK, and check my iPhone every five minutes to see if Moshi has something — hoping the Grok app one day catches up to the Claude app.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
