---
title: "From Claude Max to SuperGrok Heavy: Six Months at the Top, Then the Big Switch"
date: 2026-08-22T09:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "After months on Claude Max 20x, I switched to SuperGrok Heavy at $300/month. Herdr, Moshi, Grok Build, Grok Bot, Cursor Ultra — and the Claude mobile app I'll already miss."
categories: ["AI", "Productivity"]
tags: ["claude", "grok", "supergrok", "grok-build", "grok-bot", "cursor", "herdr", "moshi", "ai", "productivity", "claudecode", "tokens", "agents"]
cover:
  image: /images/covers/claude-max-supergrok-heavy.webp
  alt: "Claude Max to SuperGrok Heavy"
---

### Context: I'm not a casual user

When Anthropic launched **Claude Max** in April 2025, I signed up for the **20x tier at $200/month** without hesitation. Not out of snobbery — out of necessity. My workflow described in [AI-First Engineering](/posts/ai-first-engineering/) never revolved around a graphical IDE: it's **the CLI, always the CLI**. **Claude Code** and **Grok Build** in **Herdr** panes, steered from the couch via **Moshi** on iPhone, synchronized via `aictx` and orchestrated by **[HivePilot](/posts/hivepilot/)**.

I had a small **Cursor** subscription — the basic plan, barely used. Not out of principle, out of habit: my brain lives in Kitty, my agents live in **Herdr**, and my phone is a remote control via **Moshi**. I rarely type code by hand; I orchestrate context.

With **SuperGrok Heavy**, everything shifted: I now have **Cursor Ultra**, and for the first time, Cursor actually does something — but not as an IDE.

For six months, Claude Max powered **Claude Code, the Claude mobile app, and my Herdr sessions**. Then, in July 2026, I cancelled Max and subscribed to SuperGrok Heavy — and discovered **Grok Build** in my terminal, then **Grok Bot** on my iPhone.

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

### Herdr + Moshi: my actual workflow (Cursor on the sidelines — until Grok Bot)

Let's be clear: **I've never been a Cursor user in the IDE sense**. I had the small plan, I tried agentic graphical editing, and I went back to the terminal. Not a criticism — the tool is excellent for people who live in an IDE. It just wasn't *my* workflow.

That changed with **SuperGrok Heavy** — not because I suddenly adopted the IDE, but because Heavy unlocks **Cursor Ultra** and **Grok Bot**. My dormant Cursor subscription became the gateway to an agent layer I didn't have: digital teammates with their own cloud computer, reachable from iPhone.

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
| Graphical IDE / inline editing | **Cursor** | Ultra, but almost never for coding — reserved for Grok Bot |
| Autonomous delegation off-terminal | **Grok Bot** | 24/7 cloud agents, apps without APIs, native iOS |

My **skills**, hooks, plugins, and **MCP** servers (Paperless, etc.) live in my dotfiles and work in Claude Code *and* Grok Build — regardless of which Herdr pane I launch them in. Herdr doesn't wrap agents; it gives them a **persistent runtime**. Moshi doesn't replace the terminal; it gives me a **mobile window** onto that runtime.

Typical evening scenario: I launch three agents in Herdr on my Mac — one on HivePilot, one on my dotfiles, one on a blog post. I go for a run. My iPhone buzzes via Moshi: the HivePilot agent is `blocked`, it wants to confirm a `git push`. I approve from the Moshi inbox without reopening the laptop. That's my workflow. No inline diffs in an IDE — pure terminal orchestration.

What changed with the switch to Grok Heavy:

- **Grok Heavy (web/app)** → thinking, DeepSearch, real-time analysis
- **Grok Build** → new Herdr pane, same skills, Grok model
- **Grok Bot** → autonomous teammates on iPhone, dedicated cloud computer
- **Cursor Ultra** → unlocked via Heavy, used for Grok Bot — not the IDE
- **Claude Code** → still there for prod and permissions
- **Moshi** → unchanged for terminal; Grok Bot picks up off-CLI work

**Four interfaces, two ecosystems, one Herdr multiplexer — and finally a Cursor subscription that does something.**

*(Irony: this article was drafted by a Cursor Cloud Agent — via the Ultra I wasn't using before Heavy. Full circle.)*

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
| **Cloud autonomous agents** | — | **Grok Bot** (included with Heavy + Ultra) |
| **Cursor** | Small plan, unused | **Ultra** (via Heavy, for Grok Bot) |
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
- My **skills** in `dot_claude/` and `dot_agents/`? Recognized.
- My hooks, plugins, **MCP** servers (Paperless, etc.)? Recognized.
- My permission rules and repo conventions? Recognized.

I opened Grok Build in my dotfiles, and my existing agent infrastructure plugged in as-is. No migration, no rewrite. For someone who spent months wiring [skills](/posts/ai-first-engineering/), that's the killer feature — not Grok 4 Heavy itself.

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
- **Grok Build** → exploration, prototyping, tasks where I want Grok reasoning *in* the terminal — experimental refactors on HivePilot, infra scripts, multi-file investigations
- **HivePilot** → multi-agent orchestration above both, no discrimination

Grok Build's **Plan Mode** particularly won me over on risky refactors. I launch `grok` in plan mode, review each step, comment or rewrite the plan before a single line moves. Same least-privilege reflex as my Quality Gates — but native in the tool.

**Parallel subagents** also change the game on large projects. On a HivePilot refactor touching orchestrator, workers, and benchmarks, Grok Build delegates to child agents in separate worktrees. Herdr shows each pane's state in the sidebar — `working`, `blocked`, `done` — without scrolling through three terminals.

And Grok Build's **Agent Dashboard** (June 2026) looks like what Herdr already does natively: multiple parallel sessions, visibility into what each agent is doing, responding to agents waiting for approval. My multiplexer became a control room — except Herdr orchestrates it, not an IDE.

**The limits, honestly:**

- **256K token context** — well below Opus's 1M. On a massive monorepo, you feel it.
- **Still unstable beta** — I've had sessions drift into unrequested shell commands. My HivePilot guardrails and permissions remain non-negotiable.
- **No Moshi equivalent** — Grok has no `moshi-hook`. I can steer Grok Build from Moshi (it's a real terminal), but not agent-aware notifications, a unified inbox, or lock-screen approvals for Grok like Claude Code gets.

But the fact that xAI made Grok Build **Claude Code-compatible by design** says something about the market: the war is no longer about skill format, but about model quality behind it. And for me, having the choice between Opus and Grok 4.6 *in the same terminal setup* is worth part of the $300/month on its own.

### Grok Bot: the teammate who never sleeps

If Grok Build colonized my terminal, **Grok Bot** colonized my pocket — and it might be the biggest surprise of the switch.

Launched in beta on August 11, 2026, **Grok Bot** isn't a chatbot. It's a team of **named, persistent agents**, each with a job, memory, and — key point — **its own cloud Linux computer**. Not an API call chain. Not an MCP server to wire up. A real browser, real filesystem, real terminal, running 24/7 even when my MacBook is closed.

Included with **SuperGrok Heavy** and **Cursor Ultra**. Sign-in via Cursor account — hence the sudden value of my Ultra subscription, even without opening the IDE.

**How it works in practice:**

1. I create a Bot, give it a name and role ("crypto watch", "Paperless email triage", "blog prep").
2. I send it a task like a colleague — from the iOS app or desktop.
3. The Bot connects to my tools (Gmail, Notion, web interfaces without APIs) and runs the workflow end to end.
4. It comes back when it needs approval. Otherwise, it delivers.

**What sets it apart from Grok Build and Moshi:**

| | Grok Build | Moshi + Herdr | Grok Bot |
|---|---|---|---|
| **Where it runs** | My Mac / homelab | My Mac / homelab | xAI cloud (dedicated computer) |
| **Interface** | Terminal (Herdr pane) | Mobile terminal SSH/Mosh | iOS / desktop app, messaging |
| **Autonomy** | Session tied to host | Session tied to host | 24/7, laptop closed |
| **Apps without API** | Via MCP only | Via MCP only | Native browser, direct login |
| **Parallelism** | Subagents / Herdr panes | Herdr panes | Multiple independent Bots |
| **My usage** | Code, refactors, infra | Approvals, CLI steering | Watch, ops, off-terminal tasks |

The use case that sold me: **article research**. Before, I'd open the Claude mobile app on the train to brainstorm. Now I assign a Grok Bot daily crypto + tech watch. It scrapes, synthesizes, leaves a note ready in the morning. I validate from iPhone. My laptop never moved.

Another case: **ops without MCP**. Paperless has an MCP server — perfect for Claude Code in Herdr. But many tools don't. Grok Bot connects to the web UI like a human. Not architecturally elegant ([least privilege](/posts/securing-ai-agents/)? debatable), but brutally effective for one-off tasks.

The **chief of staff model** works well: one coordinator Bot, specialized Bots underneath — watch, writing, homelab monitoring. They collaborate in a thread, pass work between them, and I'm no longer the bottleneck.

**The limits, honestly:**

- **Beta, and it shows** — workflows drift, logins expire, tasks get stuck without clear notification.
- **Cursor account required** — xAI and Cursor are now linked. One more subscription to track, even if Ultra comes with Heavy.
- **No Linux desktop** — macOS, Windows, and iOS apps only. My Fedora homelab stays out of scope for now.
- **Privacy Mode** — legacy accounts must migrate to cloud storage. Worth evaluating against my [least-privilege](/posts/securing-ai-agents/) reflex.

But Grok Bot fills a gap neither Moshi nor Grok Build covered: **delegating real work off-terminal, without a host running, from iPhone**. It's the closest layer to what the Claude mobile app gave me — except the work comes back *finished*, not as conversation.

### What I actually miss: the Claude mobile app

The switch to Grok Heavy didn't make me regret the Cursor IDE — I wasn't using it for that anyway. What I *still* miss is **the Claude mobile app** for pure conversation — brainstorming, summarizing, dictating an idea without delegating a task.

With Claude Max, the iOS app was my pocket interface for everything that wasn't code: brainstorming an article, summarizing a PDF, asking a quick question on the go, dictating an idea between meetings. Clean, fast, synced with my Max account. No SSH, no Herdr, no Moshi — just Claude in my pocket.

The Grok app exists. It's improving. But today, it doesn't offer the same fluidity for everyday intellectual work outside the terminal. When I'm on the train and want to sharpen an article angle, I open Grok and... it gets the job done, without the same *presence*. Subjective, but it's the first concrete regret of the switch.

**Grok Bot fills part of the gap — but not all.** For concrete task delegation (watch, triage, prep), Grok Bot on iOS beats anything I had. For fluid conversation without a deliverable, the Claude app still leads. Moshi remains irreplaceable for steering Herdr.

| Need | Claude app (before) | Moshi + Herdr | Grok Bot (now) | Grok app (now) |
|---|---|---|---|---|
| Quick question, writing | ✅ Native, fluid | ❌ Overkill | ⚠️ Task-oriented, not chat | ⚠️ Fine, less polished |
| Steer a running CLI agent | ❌ | ✅ Inbox, push, approvals | ❌ | ❌ |
| Delegate an autonomous task | ❌ | ⚠️ Host must be on | ✅ 24/7, cloud computer | ⚠️ Limited |
| Long autonomous session | ⚠️ Limited on mobile | ✅ Agent runs on host | ✅ Independent cloud Bot | ⚠️ Web/app only |
| Apps without API/MCP | ❌ | ❌ | ✅ Native browser | ❌ |

Result: I'll probably keep a **minimal Claude Pro tier** for pocket conversation — even if Grok Bot takes over delegation. Irony: I left Max to save on terminal quota, and now I pay Heavy + Ultra + residual Claude Pro.

### The rest of what I lost

The switch has other costs beyond the extra $100 and the mobile app.

**Writing quality.** Claude writes better. Full stop. My articles still go through Claude for final review and polish — often from the mobile app or Claude Code in a Herdr pane. Grok is competent, sometimes more direct, but it lacks that *voice*.

**The MCP ecosystem on the terminal side.** **Grok Build caught up**: my [Paperless MCP servers](/posts/mcp-servers/) run in Claude Code and Grok Build without rewriting, in the same Herdr workspace. For my agentic homelab, the hub is **Herdr + Claude Code + Grok Build** — two agents, one multiplexer, one Moshi.

**Artifacts.** I use them less than before, but when I need them — diagrams, interactive documents — Claude via claude.ai or the mobile app is unbeatable. Grok has no direct equivalent.

### HivePilot still matters (maybe more than before)

Ironic twist: I built **[HivePilot](https://github.com/jsoyer/HivePilot)** to orchestrate agent swarms when a single model wasn't enough — and I still use it. Claude Code in one Herdr pane, Grok Build in another, Grok Bot in the cloud: **HivePilot** remains the layer that decides *who* does *what*, not the multiplexer that shows state.

With SuperGrok Heavy + Cursor Ultra + a residual Claude tier, the risk is no longer running out of tokens — it's launching too many agents without coordination. HivePilot doesn't discriminate by vendor: a Claude worker or a Grok worker, same contract.

### The verdict after two months

**Is SuperGrok Heavy worth $300/month?** It depends on what you're optimizing for.

- **Yes**, if you do research, multi-source analysis, reasoning on open problems, or if real-time data is critical to your work.
- **No**, if your primary use is the terminal with Claude Code — Max 20x (or even 5x) remains the best value.
- **Maybe**, if you're like me: Herdr/Moshi CLI workflow, Grok for thinking, residual Claude for your pocket.

My current setup:

```
Thinking / research / DeepSearch        →  SuperGrok Heavy (Grok 4 Heavy, grok.com)
Terminal exploration / prototyping      →  Grok Build (Herdr pane, native skills + MCP)
Autonomous delegation / watch / ops     →  Grok Bot (iOS, cloud computer, Cursor Ultra)
Sensitive repos / CI / permissions      →  Claude Code (Herdr pane, residual Pro tier)
Agent orchestration / sessions          →  Herdr (persistent multiplexer)
Mobile terminal steering / approvals    →  Moshi + moshi-hook
Quick off-terminal conversation         →  Claude app (Pro tier — keep it?)
Quick edits without an agent            →  Neovim
Multi-agent orchestration               →  HivePilot
```

The total cost far exceeds $300/month — Heavy, Ultra, residual Claude Pro. That's the price of a CLI workflow that ended up adopting Cursor — but for the Bots, not the editor.

### What this says about the 2026 market

The parallel with IDE history is striking — except for me, the IDE is the terminal. We no longer have "one AI tool" — we have an **AI stack**: **Herdr** for terminal orchestration, **Moshi** for mobile CLI steering, **Grok Build** and **Claude Code** for execution, **Grok Bot** for cloud delegation, **Grok Heavy** for thinking, **Cursor Ultra** to unlock the Bots, **HivePilot** for multi-agent orchestration, `aictx` for coherence.

The vendors know it. Anthropic pushes Max — and a mobile app I still miss for chat. xAI pushes Heavy, Grok Build, and Grok Bot. Cursor is no longer just an IDE: it's the identity infrastructure behind the Bots. Herdr and Moshi fill the terminal gap that neither Cursor nor native apps cover alone.

My prediction: by end of 2026, the question won't be "Claude or Grok?" but "which model for which surface?" — terminal via Herdr, delegation via Grok Bot, steering via Moshi, thinking via Grok Heavy — and stacked subscriptions (Heavy + Ultra + Pro) that still haven't merged.

In the meantime, I pay my bills, orchestrate my agents with HivePilot, and check my iPhone — Moshi for CLI approvals, Grok Bot for the morning watch, the Claude app for questions no Bot deserves.
