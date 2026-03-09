---
title: "Modern CLI Tools to Replace Your Defaults in 2026"
date: 2026-03-09T12:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "The definitive list of modern CLI replacements that are faster, friendlier, and smarter than the tools you grew up with."
categories: ["Tooling", "CLI"]
tags: ["cli", "terminal", "productivity", "linux", "macos", "tools", "automation"]
cover:
  image: /images/covers/modern-cli-tools.png
  alt: "Modern CLI Tools 2026"
---

Unix tools are old. `ls` was written in 1971. `grep` in 1973. `find` in 1974. They work, but they were designed for a world without colors, without Git, without multi-core processors, and without developers who expect good UX.

The Rust ecosystem changed this. Over the last decade, a wave of modern CLI tools rewrote the classics — faster, with sensible defaults, human-readable output, and better UX out of the box. Here's the ones I actually use every day.

---

### `eza` — Better `ls`

```bash
# Before
ls -la --color=auto

# After
eza -la --icons --git --group-directories-first
```

What you get: icons (with Nerd Font), inline Git status per file, proper colors, and `--tree` mode that's actually readable. I have `alias ls = eza` and `alias ll = eza -la --icons --git`.

**Install:** `brew install eza` / `cargo install eza`

---

### `bat` — Better `cat`

```bash
# Before
cat src/main.rs

# After
bat src/main.rs
```

Syntax highlighting, line numbers, Git diff decorations in the gutter, and automatic paging. Also plays well with other tools — I use it as the `MANPAGER` and `PAGER`:

```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
export BAT_THEME="Catppuccin Mocha"
```

**Install:** `brew install bat`

---

### `ripgrep` (`rg`) — Better `grep`

```bash
# Before: find all TODO in a project (slow, verbose)
grep -r "TODO" . --include="*.ts" --exclude-dir=node_modules

# After
rg "TODO" --type ts
```

Respects `.gitignore` by default, parallel search, better output formatting, and it's genuinely 5-10x faster than GNU grep on large codebases. My go-to for code search.

**Install:** `brew install ripgrep`

---

### `fd` — Better `find`

```bash
# Before
find . -name "*.rs" -not -path "*/target/*"

# After
fd -e rs
```

`fd` is `find` without the trauma. Intuitive syntax, respects `.gitignore`, colored output, parallel execution. I use it constantly with `fzf` for file pickers.

**Install:** `brew install fd`

---

### `zoxide` — Better `cd`

```bash
# Before: navigating to a deeply nested project
cd ~/projects/work/backend/services/auth

# After (after visiting once)
z auth
```

Zoxide tracks your most-visited directories and learns your habits. `z proj` jumps to wherever "proj" is, even if it's 6 levels deep. Works with Nushell, Zsh, Fish — everything.

```bash
eval "$(zoxide init zsh)"
# or in Nushell:
zoxide init nushell | save -f ~/.zoxide.nu
```

**Install:** `brew install zoxide`

---

### `atuin` — Better Shell History

This one changes how you work. Atuin replaces your shell history with a searchable database, synced across machines via an encrypted server (self-hosted or their cloud).

```bash
# Press ctrl+r — instead of a dumb reverse search, you get:
# - Full-text fuzzy search across all sessions
# - Filter by working directory, exit code, date
# - See every machine's history in one place
```

I run a self-hosted Atuin server on my Raspberry Pi. Every command I've ever typed on any machine, searchable in milliseconds.

**Install:** `brew install atuin` then `atuin register`

---

### `btop` — Better `top`

```bash
top      # 1980s vibes
htop     # better, but still limited
btop     # actually readable
```

Btop shows CPU per core, memory, disk I/O, network — all in a clean, mouse-friendly UI. I use it when I need to diagnose what's eating my RAM.

**Install:** `brew install btop`

---

### `dust` — Better `du`

```bash
# Before: which directory is eating my disk?
du -sh * | sort -rh | head -20

# After
dust -r
```

Visual tree of disk usage, sorted by size, readable at a glance. Especially useful on a Raspberry Pi where storage is limited.

**Install:** `brew install dust`

---

### `delta` — Better `git diff`

```bash
# In ~/.gitconfig
[core]
    pager = delta

[delta]
    navigate = true
    light = false
    side-by-side = true
    line-numbers = true
```

Delta is a diff viewer that makes Git diffs actually readable: syntax highlighting, side-by-side mode, better line numbers, and merge conflict markers that don't require a decoder ring.

**Install:** `brew install git-delta`

---

### `jq` / `yq` — JSON & YAML processing

Not a replacement for anything, but essential:

```bash
# Get all open PR titles from GitHub API
curl -s "https://api.github.com/repos/owner/repo/pulls" | jq '.[].title'

# Extract a value from a YAML config
yq '.database.host' config.yaml

# In Nushell, often not needed — native structured data handling
http get https://api.github.com/repos/owner/repo/pulls | get title
```

**Install:** `brew install jq yq`

---

### `mise` — One Runtime Version Manager to Rule Them All

```bash
# Instead of nvm, rbenv, pyenv, sdkman, rustup (each managing one language)
mise use node@lts
mise use python@3.12
mise use go@latest
```

One tool, every language, `.mise.toml` in the project root for per-directory versions. chezmoi manages my global `~/.config/mise/config.toml`.

**Install:** `brew install mise`

---

### The Full Install (Homebrew)

```bash
brew install eza bat ripgrep fd zoxide atuin btop dust git-delta jq yq mise
```

On Fedora:
```bash
dnf install eza bat ripgrep fd-find zoxide atuin btop dust
cargo install git-delta  # not yet in Fedora repos
```

---

*All these tools are configured and managed via my [chezmoi dotfiles](https://github.com/jsoyer)*
