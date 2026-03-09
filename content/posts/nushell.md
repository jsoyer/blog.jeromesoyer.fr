---
title: "Why I Switched to Nushell (And Why You Might Too)"
date: 2026-03-09T10:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "After years of zsh, I switched my primary shell to Nushell. Here's what changed, what broke, and why I'm not going back."
categories: ["Tooling", "Terminal"]
tags: ["nushell", "shell", "terminal", "productivity", "cli", "zsh"]
cover:
  image: /images/covers/nushell.png
  alt: "Why I Switched to Nushell"
---

There's a moment in every developer's life when they look at a bash one-liner like this:

```bash
ps aux | grep "[n]ode" | awk '{print $2}' | xargs kill
```

...and think: *there has to be a better way.*

There is. It's called **[Nushell](https://www.nushell.sh/)**, and it treats your shell like the data processing tool it actually is.

### What's Wrong With Zsh/Bash?

Nothing, technically. They work. But they were designed in an era where everything was text. Every command outputs a string, and your entire pipeline is string manipulation — `awk`, `sed`, `grep`, `cut`. You spend half your time parsing text that a machine just serialized for you.

Compare listing processes:

**Bash:**
```bash
ps aux | grep node | awk '{print $1, $2, $11}'
```

**Nushell:**
```nu
ps | where name =~ node | select user pid name
```

Same result. But in Nushell, `ps` returns a **table**. You're working with actual data — columns, types, values. No parsing required.

### The Core Idea: Everything is Structured Data

Nushell commands return tables, lists, records, or primitives. This means:

```nu
# Filter a JSON API response like a database query
http get https://api.github.com/repos/nushell/nushell/issues
  | where state == "open"
  | select title created_at user.login
  | sort-by created_at --reverse
  | first 10
```

No `jq`. No `curl | python -m json.tool`. Just... data manipulation.

### What I Use It For

**System administration:**
```nu
# Find the 5 largest directories in my home
ls ~/* | where type == dir | sort-by size --reverse | first 5 | select name size
```

**Log analysis:**
```nu
# Parse structured logs and find errors from the last hour
open /var/log/app.log
  | lines
  | each { from json }
  | where level == "error"
  | where timestamp > ((date now) - 1hr)
```

**Git workflows:**
```nu
# List branches with their last commit date
git branch -v | lines | parse "{name} {hash} {message}"
```

### The Learning Curve

Nushell is **not POSIX**. This is intentional — and it's the main thing that trips people up.

- No `&&` and `||` (use `and` and `or`, or just `;`)
- No `$VAR`, use `$env.VAR`
- No subshells with `$(...)`, use `(...)` instead
- Scripts have a different syntax than interactive commands

The first week is painful if you've been in bash for years. The second week, you start to get it. By the third week, you're annoyed when you have to use bash.

### My Setup

I use Nushell as my primary shell with:

- **Starship** for the prompt (`use ~/.config/starship/starship.nu`)
- **carapace** for completions — it generates shell completions for 500+ commands
- Custom `config.nu` for aliases, env, and PATH
- A separate `env.nu` for environment variables

Key aliases I use daily:

```nu
# In config.nu
alias ll = ls -la
alias g = git
alias v = nvim
alias dc = docker compose
```

### Compatibility: Living With Both

The hard truth: some things still need bash. Install scripts, CI pipelines, other people's code. I handle this by:

1. Keeping zsh installed as a fallback (it's macOS system default anyway)
2. Running bash scripts explicitly: `bash script.sh` — no shebang drama
3. Using `^command` in Nushell to bypass aliases and call the system command directly

### Should You Switch?

If you spend significant time in the terminal processing data, writing pipelines, or doing sysadmin work — **yes**. The productivity gains are real once you're past the learning curve.

If you're mostly running `git` commands, `npm install`, and `cd`-ing around — the switch is less compelling. Zsh works fine for that.

---

*Written while running Nushell 0.100+ on both macOS and Fedora*
