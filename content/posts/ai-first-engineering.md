---
title: "AI-First Engineering: My 650+ Skills Dotfiles Evolution"
date: 2026-04-11T09:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "How I transformed my dotfiles into an AI orchestration layer using aictx, Yapee, and over 600 custom skills."
categories: ["DevOps", "AI", "Automation"]
tags: ["aictx", "claudecode", "opencode", "codex", "dotfiles", "yapee", "automation"]
cover:
  image: /images/covers/ai-first-engineering.webp
  alt: "AI-First Engineering"
---

### The Terminal is the New IDE
In early 2026, the way we interact with code changed forever. I no longer spend most of my time typing characters; I spend it **orchestrating context**. My **[dotfiles](https://github.com/jsoyer/dotfiles)** have evolved from simple shell aliases to a comprehensive **AI Orchestration Layer**.

This is the "Least Privilege Life" applied to engineering: providing exactly the right context to the right tool at the right time.

### The Ecosystem: 190+ Agents, 650+ Skills
My environment isn't just a shell; it's a factory. I've integrated three primary AI CLI tools, all sharing a common brain managed through my dotfiles:

1.  **Claude Code:** My primary "Architect" agent. It handles deep codebase analysis and complex refactoring.
2.  **OpenCode:** A fast, extensible alternative for quick tasks and specific plugin execution via `ocx`.
3.  **Codex:** Integrated for direct logic generation and shell integration.

The core of this setup lies in the `dot_claude/` and `dot_agents/` directories, which now host **192 specialized agents** and over **650 shared skills**. Whether I'm on Fedora or Windows, my AI assistants have the same capabilities and the same memory.

### The Secret Sauce: `aictx` & `Yapee`
Synchronization is the hardest part of multi-tool AI workflows. This is where two new projects in my ecosystem come in:

*   **[`aictx`](https://github.com/jsoyer/dotfiles/releases/tag/aictx-v0.3.0) (v0.3.0):** This utility acts as a **Context Source of Truth**. It manages the state and history between my different CLIs, ensuring that if Claude makes a decision, OpenCode and Codex are aware of it. No more repeated prompts.
*   **`Yapee`:** My automation handler. It connects my AI agents to my infrastructure. `Yapee` is the one triggering my **Synapse Forge** deployments or updating my **Homebrew Tap** when an agent finishes a build.

### Optimization: RTK & Quality Gates
To avoid "context bloat" and keep costs (and token usage) under control, I’ve implemented **RTK (Token Optimization Proxy)**. 

Through custom event hooks in my dotfiles, I’ve set up **Quality Gates**. Before an agent can execute a major change, it must pass a validation check handled by a separate agent. This "Least Privilege" for code execution ensures that my AI fleet doesn't go rogue on my infrastructure.

### The Result: Flow State 2.0
With this setup, I don't "use" AI; I **collaborate** with it. By having my skills and agents defined as code in my dotfiles, I can provision a new machine (like my recent Mac cluster) and be fully productive with my entire AI-First workflow in under 5 minutes.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
