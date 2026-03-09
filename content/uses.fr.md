---
title: "Outils"
date: 2026-03-09
draft: false
hidemeta: true
showtoc: true
description: "Le matériel, les logiciels et les outils que j'utilise vraiment tous les jours."
---

Un document vivant de mon setup. Mis à jour quand quelque chose change.

---

## Matériel

- **MacBook Pro** — machine principale
- **Mac Mini** — serveur maison / poste de travail secondaire
- **Raspberry Pi** — auto-hébergement, expérimentation
- **Framework Laptop** — sous Fedora Atomic

---

## Systèmes d'exploitation

- **macOS** — machine principale
- **Fedora Atomic** (Silverblue) — laptop Framework, OS immuable
- **Fedora** — poste de travail bureau
- **Raspberry Pi OS** (basé Debian) — cluster Pi

---

## Terminal & Shell

- **[Kitty](https://sw.kovidgoyal.net/kitty/)** — terminal principal. GPU-accéléré, scriptable via `kitten`, rapide.
- **[WezTerm](https://wezfurlong.org/wezterm/)** — terminal de secours, configurable en Lua
- **[Nushell](https://www.nushell.sh/)** — shell principal. Données structurées, pipelines typés, fini les acrobaties `awk`.
- **[Zsh](https://www.zsh.org/)** + Oh-My-Zsh + Powerlevel10k — shell de secours sur les machines où Nushell n'est pas encore configuré
- **[Starship](https://starship.rs/)** — prompt cross-shell (utilisé avec Nushell)

**Remplaçants CLI modernes :**

| Classique | Remplacement | Pourquoi |
|-----------|-------------|----------|
| `ls` | [eza](https://github.com/eza-community/eza) | Couleurs, icons, statut git |
| `cat` | [bat](https://github.com/sharkdp/bat) | Syntax highlighting, pagination |
| `grep` | [ripgrep](https://github.com/BurntSushi/ripgrep) | Vitesse |
| `find` | [fd](https://github.com/sharkdp/fd) | Syntaxe plus simple |
| `cd` | [zoxide](https://github.com/ajeetdsoutu/zoxide) | Saut intelligent |
| `history` | [atuin](https://atuin.sh/) | Searchable, synchronisé entre machines |
| `top` | [btop](https://github.com/aristocratstech/btop) | Vraiment lisible |
| `du` | [dust](https://github.com/bootandy/dust) | Usage disque visuel |
| `curl` | [httpie](https://httpie.io/) / [xh](https://github.com/ducaale/xh) | HTTP lisible par un humain |

---

## Éditeur

- **[Neovim](https://neovim.io/)** — pour tout. LSP, Git, fuzzy find, tout le reste.
- Config gérée via chezmoi, setup Lua complet.

Plugins clés :
- **lazy.nvim** — gestionnaire de plugins
- **nvim-lspconfig** — setup LSP
- **nvim-treesitter** — syntaxe + édition structurelle
- **telescope.nvim** — fuzzy finder
- **oil.nvim** — explorateur de fichiers comme un buffer
- **gitsigns.nvim** — décorations git inline

---

## Spécifique macOS

- **[Aerospace](https://github.com/nikitabobko/AeroSpace)** — gestionnaire de fenêtres en tiling. Piloté au clavier, config-as-code, sans interface graphique inutile.
- **[Sketchybar](https://felixkratz.github.io/SketchyBar/)** — barre de statut entièrement scriptable
- **[Raycast](https://www.raycast.com/)** — lanceur d'applications + extensions, dont ma propre **[extension Kitty](https://github.com/jsoyer/raycast-kitty)**
- **[Homebrew](https://brew.sh/)** — gestionnaire de paquets
- **[Wipey](https://github.com/jsoyer/Wipey)** — ma propre app Swift pour verrouiller clavier/trackpad/écran pendant le nettoyage

---

## Dotfiles & Gestion de la configuration

- **[chezmoi](https://www.chezmoi.io/)** — gère tous les fichiers de config sur chaque machine
- Sauvegardé sur Git, auto-commit + auto-push activés
- Templates Go pour la config spécifique à chaque plateforme
- Une seule commande de bootstrap pour passer de zéro à productif sur une nouvelle machine

Voir mon [article sur les dotfiles](/fr/posts/dotfiles/) pour le détail complet.

---

## Développement

- **[Docker](https://www.docker.com/)** — containers pour tout ce que je ne veux pas polluer mon système
- **[mise](https://mise.jdx.dev/)** — gestionnaire de versions de runtimes (remplace nvm, rbenv, pyenv, tous)
- **[just](https://github.com/casey/just)** — lanceur de commandes, plus simple que les Makefiles
- **[jq](https://stedolan.github.io/jq/)** / **[yq](https://github.com/mikefarah/yq)** — traitement JSON/YAML
- **[RTK](https://github.com/jsoyer/rtk)** — mon propre proxy CLI qui réduit la consommation de tokens LLM de 60-90% sur les commandes dev

---

## Homelab (Raspberry Pi)

- **[Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)** — gestion de documents, OCR, recherche plein texte
- **[Grafana](https://grafana.com/)** + InfluxDB — dashboards de monitoring (dont les données de sommeil Philips Somneo)
- **[UniFi](https://ui.com/)** — gestion réseau (oui, c'est surdimensionné pour une maison)
- **[Legendary Minecraft](https://github.com/jsoyer/Legendary-Java-Minecraft-Geyser-Floodgate)** — serveur auto-hébergé Java + Bedrock

---

## Ce blog

- **[Hugo](https://gohugo.io/)** — générateur de site statique
- **[PaperMod](https://github.com/adityatelange/hugo-PaperMod)** — thème avec CSS Catppuccin personnalisé
- **[Cloudflare Pages](https://pages.cloudflare.com/)** — hébergement
- **GitHub Actions** — CI/CD (build + déploiement au push sur `main`)

---

*Dernière mise à jour : mars 2026*
