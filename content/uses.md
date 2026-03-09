---
title: "Uses"
date: 2026-03-09
draft: false
hidemeta: true
showtoc: true
description: "The hardware, software, and tools I actually use every day."
---

A living document of my setup. Updated when something changes.

---

## Hardware

- **MacBook Pro** — daily driver
- **Mac Mini** — home server / secondary workstation
- **Raspberry Pi** — self-hosting, experimentation
- **Framework Laptop** — running Fedora Atomic

---

## Operating Systems

- **macOS** — main machine
- **Fedora Atomic** (Silverblue) — Framework laptop, immutable OS
- **Fedora** — desktop workstation
- **Raspberry Pi OS** (Debian-based) — Pi cluster

---

## Terminal & Shell

- **[Kitty](https://sw.kovidgoyal.net/kitty/)** — primary terminal. GPU-accelerated, scriptable via `kitten`, fast.
- **[WezTerm](https://wezfurlong.org/wezterm/)** — backup terminal, Lua-configurable
- **[Nushell](https://www.nushell.sh/)** — primary shell. Structured data, typed pipelines, no more `awk` gymnastics.
- **[Zsh](https://www.zsh.org/)** + Oh-My-Zsh + Powerlevel10k — fallback shell on machines where Nushell isn't yet set up
- **[Starship](https://starship.rs/)** — cross-shell prompt (used in Nushell)

**Modern CLI replacements:**

| Classic | Replacement | Why |
|---------|-------------|-----|
| `ls` | [eza](https://github.com/eza-community/eza) | Colors, icons, git status |
| `cat` | [bat](https://github.com/sharkdp/bat) | Syntax highlighting, paging |
| `grep` | [ripgrep](https://github.com/BurntSushi/ripgrep) | Speed |
| `find` | [fd](https://github.com/sharkdp/fd) | Simpler syntax |
| `cd` | [zoxide](https://github.com/ajeetdsouza/zoxide) | Smart jump |
| `history` | [atuin](https://atuin.sh/) | Searchable, synced across machines |
| `top` | [btop](https://github.com/aristocratstech/btop) | Actually readable |
| `du` | [dust](https://github.com/bootandy/dust) | Visual disk usage |
| `curl` | [httpie](https://httpie.io/) / [xh](https://github.com/ducaale/xh) | Human-friendly HTTP |

---

## Editor

- **[Neovim](https://neovim.io/)** — everything. LSP, Git, fuzzy find, the works.
- Config managed via chezmoi, full Lua setup.

Key plugins:
- **lazy.nvim** — plugin manager
- **nvim-lspconfig** — LSP setup
- **nvim-treesitter** — syntax + structural editing
- **telescope.nvim** — fuzzy finder
- **oil.nvim** — file explorer as a buffer
- **gitsigns.nvim** — git decorations inline

---

## macOS Specific

- **[Aerospace](https://github.com/nikitabobko/AeroSpace)** — tiling window manager. Keyboard-driven, config-as-code, no GUI nonsense.
- **[Sketchybar](https://felixkratz.github.io/SketchyBar/)** — fully scriptable status bar
- **[Raycast](https://www.raycast.com/)** — app launcher + extensions, including my own **[Kitty extension](https://github.com/jsoyer/raycast-kitty)**
- **[Homebrew](https://brew.sh/)** — package manager
- **[Wipey](https://github.com/jsoyer/Wipey)** — my own Swift app to lock keyboard/trackpad/screen for cleaning

---

## Dotfiles & Configuration Management

- **[chezmoi](https://www.chezmoi.io/)** — manages all config files across every machine
- Git-backed, auto-commit + auto-push enabled
- Go templates for platform-specific config
- One bootstrap command to go from zero to productive on a new machine

See my [dotfiles article](/posts/dotfiles/) for the full breakdown.

---

## Development

- **[Docker](https://www.docker.com/)** — containers for everything I don't want polluting my system
- **[mise](https://mise.jdx.dev/)** — runtime version manager (replaces nvm, rbenv, pyenv, all of them)
- **[just](https://github.com/casey/just)** — command runner, simpler than Makefiles
- **[jq](https://stedolan.github.io/jq/)** / **[yq](https://github.com/mikefarah/yq)** — JSON/YAML processing
- **[RTK](https://github.com/jsoyer/rtk)** — my own CLI proxy that cuts LLM token consumption by 60-90% on dev commands

---

## Homelab (Raspberry Pi)

- **[Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)** — document management, OCR, full-text search
- **[Grafana](https://grafana.com/)** + InfluxDB — monitoring dashboards (including Philips Somneo sleep data)
- **[UniFi](https://ui.com/)** — network management (yes, it's overkill for a home)
- **[Legendary Minecraft](https://github.com/jsoyer/Legendary-Java-Minecraft-Geyser-Floodgate)** — self-hosted Java+Bedrock server

---

## This Blog

- **[Hugo](https://gohugo.io/)** — static site generator
- **[PaperMod](https://github.com/adityatelange/hugo-PaperMod)** — theme with custom Catppuccin CSS
- **[Cloudflare Pages](https://pages.cloudflare.com/)** — hosting
- **GitHub Actions** — CI/CD (build + deploy on push to `main`)

---

*Last updated: March 2026*
