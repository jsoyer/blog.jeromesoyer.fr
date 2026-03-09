---
title: "RTK: I Built a Rust Proxy to Stop Burning Tokens on Git Status"
date: 2026-03-09T15:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "How I built a CLI proxy in Rust that cuts LLM token consumption by 60-90% on common dev operations — and why it matters more than you think."
categories: ["Tooling", "AI"]
tags: ["rust", "cli", "llm", "claude", "ai", "productivity", "tokens", "automation"]
---

If you use Claude Code, Cursor, or any AI-assisted dev tool daily, here's a number that should bother you: **a single `git status` on a large repo can consume 10,000+ tokens**. Not because the output is useful — but because the raw text gets shoved into context as-is.

I built **[RTK](https://github.com/jsoyer/rtk)** (Rust Token Killer) to fix this. It's a CLI proxy that sits between your commands and your LLM, filtering and compressing output before it hits the context window. Single Rust binary, zero dependencies, 60-90% token savings on common dev operations.

### The Problem

Watch what happens when you run `git log --oneline` on a repo with 500 commits inside Claude Code:

```
commit abc1234 fix: update dependency
commit def5678 feat: add new endpoint
commit ghi9012 chore: update lockfile
... (497 more lines)
```

The LLM gets all 500 lines. It needs maybe the last 10. You just burned ~15,000 tokens for noise.

Same with `docker ps`, `npm list`, `ls -la` on a busy directory. These commands produce verbose output that's mostly irrelevant to the task at hand. The AI doesn't need the full dump — it needs a signal.

### How RTK Works

RTK acts as a transparent proxy with command-specific filters:

```bash
# Without RTK: raw output, full token cost
git log --oneline  # 500 lines → ~15k tokens

# With RTK: filtered, compressed output
rtk git log --oneline  # last 20 lines + summary → ~800 tokens
```

The hook-based integration makes it completely transparent — you never call `rtk` directly after setup. Your existing commands are automatically rewritten:

```bash
# In your shell config (managed by chezmoi, naturally)
# Claude Code hook rewrites: git status → rtk git status
```

### Commands That Benefit Most

RTK has filters for the operations that generate the most token waste:

**Git operations:**
```bash
rtk git status      # strips untracked file lists when > 20 files
rtk git log         # limits to last 20 commits, compresses format
rtk git diff        # summarizes large diffs, keeps context
```

**System commands:**
```bash
rtk docker ps       # strips headers, formats as compact table
rtk npm list        # shows only direct dependencies
rtk ls              # limits output, groups by type
```

**Process output:**
```bash
rtk ps aux          # filters to relevant processes
rtk cat             # truncates large files with summary
```

### The Analytics

The part I find most satisfying: RTK tracks everything.

```bash
rtk gain
# Token Savings Report
# ─────────────────────────────────────
# Total commands proxied:    1,247
# Total tokens saved:        2,847,392
# Average savings per cmd:   68.3%
# Biggest win: git log       94.1%
# ─────────────────────────────────────
# Estimated cost saved:      ~$8.54

rtk gain --history
# Shows per-command breakdown with timestamps

rtk discover
# Analyzes your Claude Code history
# Found 47 commands that could have been proxied
# Estimated missed savings: 340,000 tokens
```

`rtk discover` is particularly useful — it parses your Claude Code session history and tells you which commands you ran unproxied and what you could have saved.

### Why Rust?

Single binary, zero dependencies, sub-millisecond overhead. The proxy needs to be completely invisible — if it adds any perceptible latency to your commands, you'll stop using it. Rust made the performance constraint trivial.

```bash
# RTK overhead on git status
hyperfine 'git status' 'rtk git status'
# git status:     12.3ms
# rtk git status: 13.1ms  (+0.8ms — imperceptible)
```

### Installation

```bash
# From GitHub releases (recommended)
curl -sL https://github.com/jsoyer/rtk/releases/latest/download/rtk-linux-x86_64 -o ~/.local/bin/rtk
chmod +x ~/.local/bin/rtk

# Or build from source
git clone https://github.com/jsoyer/rtk
cd rtk && cargo build --release
cp target/release/rtk ~/.local/bin/
```

Then configure the Claude Code hook in `~/.claude/settings.json` — RTK's README has the exact snippet.

### The Bigger Picture

Token costs seem abstract until you run `rtk gain` after a week of heavy Claude Code usage and see you've saved 3 million tokens. At current API prices, that's real money. More importantly, a leaner context window means the model has more room for the stuff that actually matters — your code, your question, your intent.

The best tools are the ones that disappear. RTK runs silently in the background, and the only time you notice it is when you check the savings report and wonder how you tolerated the noise before.

---

**Source code**: [github.com/jsoyer/rtk](https://github.com/jsoyer/rtk) — PRs and issues welcome.
