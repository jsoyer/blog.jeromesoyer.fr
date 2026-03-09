---
title: "mise: One Tool to Replace nvm, rbenv, pyenv, and Every Other Version Manager"
date: 2026-03-09T20:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "mise consolidates all language version managers into a single CLI tool with .mise.toml config."
categories: ["Tooling", "DevOps"]
tags: ["mise", "cli", "automation", "productivity", "node", "python", "ruby", "go"]
cover:
  image: /images/covers/mise.webp
  alt: "mise runtime version manager"
---

I've spent years drowning in a sea of version managers. `nvm` for Node, `rbenv` for Ruby, `pyenv` for Python, `gvm` for Go, and don't even get me started on finding whatever chaos manages your Rust binaries. Each one adds shell hooks, each one is slow to load, and each one requires its own setup ritual. Then you jump between projects and realize you're running Node 16 when this repo needs 20. Nightmare.

Enter `mise` — a single binary that replaces *all of them*.

## The Problem with Multiple Version Managers

The fundamental issue isn't that these tools are bad. `nvm` works fine, `pyenv` is solid. The problem is fragmentation. You end up with:

- Multiple shell initialization hooks (slow startup)
- Different config formats (some use `.nvmrc`, some `.python-version`)
- Manual version switching per project
- No unified way to see what's installed globally vs. locally
- Sharing version requirements across projects is messy

I've seen teams lose hours to "it works on my machine" because someone had a different Node version without knowing it.

## mise: One Tool, All Runtimes

`mise` is written in Rust and does one job extremely well: manage runtime versions across any language. It works through a single `.mise.toml` file per project (which you version control), and a global config file for defaults.

Installation is straightforward:

```bash
curl https://mise.jdx.dev/install.sh | sh
```

Setup a new project:

```bash
mise use node@22 python@3.12 go@latest
```

This creates a `.mise.toml` in your project:

```toml
[tools]
node = "22"
python = "3.12"
go = "latest"
```

Commit this file. Now, anyone cloning the repo runs `mise` and gets the exact same versions automatically. No guessing, no version mismatch nightmares.

## Global Defaults with chezmoi

For my machine setup, I keep a global mise config at `~/.config/mise/config.toml`. Since I manage my dotfiles with `chezmoi`, I template it to vary between my macOS laptop and Fedora Atomic workstation:

```toml
# ~/.config/mise/config.toml (chezmoi template)
[tools]
node = "{{ .node_version }}"
python = "{{ .python_version }}"
rust = "stable"

{{ if eq .chezmoi.os "darwin" }}
# macOS gets Xcode tools
{{ else if eq .chezmoi.osRelease.id "fedora" }}
# Fedora Atomic gets minimal baseline
{{ end }}
```

The `.chezmoi.toml.tmpl` defines the versions:

```toml
[node_version]
node_version = "22"
python_version = "3.12"
```

After `chezmoi apply`, my mise defaults are consistent across machines.

## Performance: No More Shell Slowdown

`nvm` is notorious for slowing down shell startup because it hooks into every new shell invocation. `mise` is different—it's a fast binary with minimal overhead. I've measured shell startup time dropping by 50-100ms on my machines after switching away from `nvm`.

`mise` also respects the standard shims (it drops executables in `~/.local/share/mise/shims`), so tools just work without re-initialization.

## Bonus: Task Runner

`mise` includes a lightweight task runner. Instead of a Makefile, you can define tasks in `.mise.toml`:

```toml
[tasks.test]
run = "npm test"

[tasks.build]
run = "npm run build && cargo build"

[tasks.dev]
run = "npm run dev"
```

Then:

```bash
mise run test
mise run build
```

Not a Makefile replacement for complex projects, but perfect for simple project workflows.

## The Reality Check

`mise` isn't perfect. The ecosystem is still maturing—some less common runtimes don't have plugins yet. But for Node, Python, Ruby, Go, Rust, and most common languages? It's rock-solid.

The biggest win: one config file per project, one global config, one tool. No more shell initialization chaos, no more version mismatch bugs, no more "but it worked locally."

If you're juggling multiple version managers, give `mise` an honest try. The relief is immediate.
