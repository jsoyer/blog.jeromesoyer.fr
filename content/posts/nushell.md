---
title: "Why I Switched to Nushell (And Why You Might Too)"
date: 2026-03-09T10:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "After years of zsh, I switched my primary shell to Nushell. Here's what changed, what broke, and why I'm not going back."
categories: ["Tooling", "Terminal"]
tags: ["nushell", "shell", "terminal", "productivity", "cli", "zsh"]
---

# [EN] Why I Switched to Nushell (And Why You Might Too)

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

# [FR] Pourquoi j'ai switché sur Nushell (et pourquoi vous devriez peut-être aussi)

Il y a un moment dans la vie de tout développeur où on regarde une ligne bash comme ça :

```bash
ps aux | grep "[n]ode" | awk '{print $2}' | xargs kill
```

...et on se dit : *il doit y avoir mieux.*

Il y a. Ça s'appelle **[Nushell](https://www.nushell.sh/)**, et ça traite votre shell comme l'outil de traitement de données qu'il est vraiment.

### Le problème avec Bash/Zsh ?

Rien, techniquement. Ça marche. Mais ils ont été conçus à une époque où tout était du texte. Chaque commande sort une chaîne de caractères, et toute votre pipeline est de la manipulation de texte — `awk`, `sed`, `grep`, `cut`. Vous passez la moitié du temps à parser du texte qu'une machine vient de sérialiser pour vous.

### L'idée centrale : tout est données structurées

En Nushell, les commandes retournent des tables, des listes, des enregistrements. Ça change tout :

```nu
# Filtrer une réponse API comme une requête SQL
http get https://api.github.com/repos/nushell/nushell/issues
  | where state == "open"
  | select title created_at user.login
  | sort-by created_at --reverse
  | first 10
```

Pas de `jq`. Pas de `curl | python -m json.tool`. Juste... de la manipulation de données.

### La courbe d'apprentissage

Nushell n'est **pas POSIX**. C'est voulu — et c'est ce qui perturbe le plus au début.

- Pas de `&&` et `||` (utilisez `and`/`or`)
- Pas de `$VAR`, mais `$env.VAR`
- Syntaxe différente pour les scripts et l'interactif

La première semaine est difficile si vous êtes en bash depuis des années. La troisième semaine, vous êtes agacé quand vous devez retourner en bash.

### Verdict

Si vous traitez beaucoup de données en terminal, construisez des pipelines complexes, ou faites de l'admin sys — **le switch vaut le coup**. Les gains de productivité sont réels une fois la courbe passée.

---

*Written while running Nushell 0.100+ on both macOS and Fedora*
