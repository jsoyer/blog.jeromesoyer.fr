---
title: "chezmoi vs yadm vs stow: Which Dotfiles Manager Should You Use in 2026?"
date: 2026-03-09T13:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "A practical comparison of the three most popular dotfiles managers — with real tradeoffs, not just feature tables."
categories: ["DevOps", "Tooling"]
tags: ["chezmoi", "dotfiles", "yadm", "stow", "automation", "linux", "macos"]
---

# chezmoi vs yadm vs stow: Which Dotfiles Manager Should You Use in 2026?

I've used all three. I settled on chezmoi. But the honest answer is: *it depends on what you're trying to do*. Here's the practical breakdown, based on actual usage across macOS, Fedora, Fedora Atomic, and Raspberry Pi.

> Already know chezmoi? See [my full dotfiles setup here](/posts/dotfiles/).

---

### What Problem Are We Solving?

Dotfiles are the config files that live in your home directory: `.zshrc`, `.gitconfig`, `~/.config/nvim/`, etc. The problem:

1. They're scattered across your filesystem
2. You want them version-controlled
3. You want them consistent across multiple machines
4. Some values differ per machine (work laptop vs personal, macOS vs Linux)
5. Some files contain secrets that shouldn't be in git

Every dotfiles manager solves problems 1 and 2 easily. Problems 3, 4, and 5 are where they diverge.

---

### GNU Stow

**The approach:** symlinks. Stow creates symlinks from a managed directory (`~/dotfiles/`) to your home directory.

```bash
# Structure
~/dotfiles/
  zsh/.zshrc           → ~/.zshrc
  nvim/.config/nvim/   → ~/.config/nvim/

# Apply
stow zsh
stow nvim
```

**What it does well:**
- Conceptually simple — you understand exactly what it does
- No magic, no special file format
- Files are real files in a Git repo
- Works on anything with a POSIX shell

**Where it falls short:**
- No templating — same file on every machine
- No secrets management
- No setup scripts
- Managing the symlink tree gets messy with complex configs

**Who it's for:** Single machine, or multiple identical machines. If you have one Linux box and want your configs in Git, Stow is perfect. If you have macOS + Linux + a Pi, you'll quickly outgrow it.

---

### yadm (Yet Another Dotfiles Manager)

**The approach:** a Git wrapper. yadm treats your home directory as a Git repository, with support for alternates (machine-specific files) and encryption.

```bash
yadm init
yadm add ~/.zshrc ~/.gitconfig
yadm commit -m "initial"
yadm push
```

**What it does well:**
- Almost zero learning curve if you know Git
- Alternates: `~/.zshrc##os.Darwin` vs `~/.zshrc##os.Linux`
- Built-in encryption via GPG
- Bootstrap scripts via `~/.config/yadm/bootstrap`

**Where it falls short:**
- Alternates are filename-based, which gets unwieldy with many variations
- Less active development (last major release 2023)
- No first-class templating (it has Jinja2 support but it's bolted on)
- The "whole home dir as a repo" mental model is slightly odd

**Who it's for:** Single developer who wants Git-native dotfiles management with minimal new tooling to learn. Excellent choice for a straightforward setup.

---

### chezmoi

**The approach:** a dedicated state machine. chezmoi manages a source directory (`~/.local/share/chezmoi/`) and applies it to your home directory. It explicitly tracks what *should* be there, diffs against what *is* there, and applies changes.

```bash
chezmoi add ~/.zshrc
chezmoi edit ~/.zshrc   # edits the source, not the live file
chezmoi apply           # applies changes
chezmoi diff            # shows what would change
```

**What it does well:**
- Go templates: one file, different content per machine
- Scripts: run on first apply, on change, or every time
- Multiple encryption backends (GPG, age, 1Password, Bitwarden)
- External files: pull dotfiles from URLs or git repos
- `chezmoi diff` before applying — you always see what will change
- Active development, strong community

**Where it falls short:**
- Learning curve: the source directory naming conventions take getting used to (`dot_`, `executable_`, `private_`, `.tmpl`)
- It's a new mental model — editing `~/.zshrc` doesn't change the chezmoi source automatically (you need `chezmoi re-add`)
- Overkill for a single machine

**Who it's for:** Multi-machine, multi-OS setups. If you need the same dotfiles to work differently on macOS, Fedora, and a Pi — chezmoi is the right tool.

---

### Side-by-Side Comparison

| Feature | Stow | yadm | chezmoi |
|---------|------|------|---------|
| **Approach** | Symlinks | Git wrapper | State machine |
| **Templating** | ❌ | Limited (Jinja2) | ✅ Go templates |
| **Setup scripts** | ❌ | ✅ Bootstrap | ✅ .chezmoiscripts |
| **Encryption** | ❌ | ✅ GPG | ✅ GPG, age, 1Password... |
| **Multi-OS support** | Manual | Alternates (filename) | Templates (conditional logic) |
| **Learning curve** | Low | Low-Medium | Medium |
| **Active dev** | Stable/maintained | Slower | ✅ Very active |
| **External sources** | ❌ | ❌ | ✅ |
| **Auto-commit/push** | ❌ | Via Git | ✅ Built-in |

---

### My Decision: chezmoi

I run the same dotfiles on 5+ machines across 4 OSes. The template system is the deciding factor:

```toml
# .chezmoi.toml.tmpl
[data]
  profile = {{ promptString "profile (mac/linux/rpi/windows)" | quote }}
```

```bash
# dot_zshrc.tmpl
{{ if eq .chezmoi.os "darwin" }}
eval "$(/opt/homebrew/bin/brew shellenv)"
{{ else if eq .profile "rpi" }}
export PATH="$HOME/.local/bin:$PATH"
{{ end }}
```

One file. Works everywhere. The Stow alternative would be maintaining 4 separate `.zshrc` files and manually keeping them in sync. With yadm, I'd have 4 alternates and still duplicate most of the content.

The auto-commit/push feature is also a killer feature for daily use — I `chezmoi re-add` and my changes are in Git, pushed to GitHub, ready for my other machines.

---

### Quick Decision Guide

```
Single machine? → Stow (simple) or yadm (Git-native)
Multiple machines, same OS? → yadm
Multiple machines, multiple OS? → chezmoi
Need to manage secrets? → chezmoi or yadm
Want zero new mental models? → yadm
Want maximum power? → chezmoi
```

---

*See [my full chezmoi setup](/posts/dotfiles/) for the detailed implementation*
