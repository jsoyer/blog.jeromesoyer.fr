---
title: "Les outils CLI modernes pour remplacer vos classiques en 2026"
date: 2026-03-09T12:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "La liste définitive des remplaçants CLI modernes — plus rapides, plus ergonomiques, et plus intelligents que les outils avec lesquels vous avez grandi."
categories: ["Tooling", "CLI"]
tags: ["cli", "terminal", "productivity", "linux", "macos", "tools", "automation"]
---

# Les outils CLI modernes pour remplacer vos classiques en 2026

Les outils Unix sont vieux. `ls` date de 1971. `grep` de 1973. `find` de 1974. Ils fonctionnent, mais ils ont été conçus pour un monde sans couleurs, sans Git, sans processeurs multi-cœurs, et sans développeurs qui attendent une bonne UX.

L'écosystème Rust a changé la donne. Voici ceux que j'utilise vraiment tous les jours.

---

### `eza` — Mieux que `ls`

```bash
# Avant
ls -la --color=auto

# Après
eza -la --icons --git --group-directories-first
```

Ce qu'on gagne : icons (avec Nerd Font), statut Git par fichier, couleurs correctes, et un mode `--tree` vraiment lisible. J'ai `alias ls = eza` et `alias ll = eza -la --icons --git`.

**Install :** `brew install eza` / `cargo install eza`

---

### `bat` — Mieux que `cat`

```bash
# Avant
cat src/main.rs

# Après
bat src/main.rs
```

Syntax highlighting, numéros de ligne, décorations de diff Git dans la marge, et pagination automatique. Je l'utilise aussi comme `MANPAGER` et `PAGER` :

```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
export BAT_THEME="Catppuccin Mocha"
```

**Install :** `brew install bat`

---

### `ripgrep` (`rg`) — Mieux que `grep`

```bash
# Avant : trouver tous les TODO dans un projet (lent, verbeux)
grep -r "TODO" . --include="*.ts" --exclude-dir=node_modules

# Après
rg "TODO" --type ts
```

Respecte `.gitignore` par défaut, recherche parallèle, meilleur formatage de sortie, et vraiment 5-10x plus rapide que GNU grep sur les gros projets.

**Install :** `brew install ripgrep`

---

### `fd` — Mieux que `find`

```bash
# Avant
find . -name "*.rs" -not -path "*/target/*"

# Après
fd -e rs
```

`fd`, c'est `find` sans le traumatisme. Syntaxe intuitive, respecte `.gitignore`, sortie colorée, exécution parallèle.

**Install :** `brew install fd`

---

### `zoxide` — Mieux que `cd`

```bash
# Avant : naviguer vers un projet profondément imbriqué
cd ~/projects/work/backend/services/auth

# Après (après une première visite)
z auth
```

Zoxide trace vos répertoires les plus visités et apprend vos habitudes. `z proj` saute là où "proj" se trouve, même à 6 niveaux de profondeur.

```bash
eval "$(zoxide init zsh)"
# ou en Nushell :
zoxide init nushell | save -f ~/.zoxide.nu
```

**Install :** `brew install zoxide`

---

### `atuin` — Mieux que l'historique shell

Celui-ci change votre façon de travailler. Atuin remplace votre historique shell par une base de données searchable, synchronisée entre machines via un serveur chiffré (auto-hébergé ou leur cloud).

```bash
# Appuyez sur ctrl+r — au lieu d'une recherche inversée basique, vous obtenez :
# - Recherche fuzzy plein texte sur toutes les sessions
# - Filtrage par répertoire de travail, code de sortie, date
# - L'historique de toutes vos machines en un seul endroit
```

Je fais tourner un serveur Atuin auto-hébergé sur mon Raspberry Pi.

**Install :** `brew install atuin` puis `atuin register`

---

### `btop` — Mieux que `top`

```bash
top      # ambiance années 80
htop     # mieux, mais toujours limité
btop     # vraiment lisible
```

Btop affiche le CPU par cœur, la mémoire, les I/O disque, le réseau — tout dans une interface propre et compatible souris.

**Install :** `brew install btop`

---

### `dust` — Mieux que `du`

```bash
# Avant : quel répertoire mange mon disque ?
du -sh * | sort -rh | head -20

# Après
dust -r
```

Arborescence visuelle de l'utilisation du disque, triée par taille, lisible d'un coup d'œil.

**Install :** `brew install dust`

---

### `delta` — Mieux que `git diff`

```bash
# Dans ~/.gitconfig
[core]
    pager = delta

[delta]
    navigate = true
    light = false
    side-by-side = true
    line-numbers = true
```

Delta est un visualiseur de diff qui rend les diffs Git vraiment lisibles : syntax highlighting, mode côte-à-côte, meilleurs numéros de ligne.

**Install :** `brew install git-delta`

---

### `jq` / `yq` — Traitement JSON & YAML

Pas des remplaçants, mais essentiels :

```bash
# Obtenir tous les titres de PR ouverts depuis l'API GitHub
curl -s "https://api.github.com/repos/owner/repo/pulls" | jq '.[].title'

# Extraire une valeur d'une config YAML
yq '.database.host' config.yaml
```

**Install :** `brew install jq yq`

---

### `mise` — Un gestionnaire de versions pour tout

```bash
# Au lieu de nvm, rbenv, pyenv, sdkman, rustup (chacun gérant un seul langage)
mise use node@lts
mise use python@3.12
mise use go@latest
```

Un outil, tous les langages, `.mise.toml` à la racine du projet pour des versions par répertoire.

**Install :** `brew install mise`

---

### L'install complète (Homebrew)

```bash
brew install eza bat ripgrep fd zoxide atuin btop dust git-delta jq yq mise
```

Sur Fedora :
```bash
dnf install eza bat ripgrep fd-find zoxide atuin btop dust
cargo install git-delta  # pas encore dans les dépôts Fedora
```

---

| Classique | Remplacement | Gain principal |
|-----------|-------------|----------------|
| `ls` | `eza` | Icons, git status, tree lisible |
| `cat` | `bat` | Syntax highlighting, gutter diff |
| `grep` | `ripgrep` | 5-10x plus rapide, respecte .gitignore |
| `find` | `fd` | Syntaxe intuitive, parallèle |
| `cd` | `zoxide` | Navigation intelligente par apprentissage |
| `history` | `atuin` | Base de données searchable, sync multi-machine |
| `top` | `btop` | Interface lisible, souris, stats complètes |
| `du` | `dust` | Vue arborescente visuelle |
| `git diff` | `delta` | Syntax highlighting, side-by-side |

---

*Tous ces outils sont configurés et gérés via mes [dotfiles chezmoi](https://github.com/jsoyer)*
