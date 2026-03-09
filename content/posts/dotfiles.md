---
title: "Dotfiles Revolution: How I Manage My Entire dev Environment with Chezmoi"
date: 2026-02-14T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "A comprehensive guide to cross-platform dotfiles management"
categories: ["DevOps", "Linux", "macOS"]
tags: ["chezmoi", "dotfiles", "automation", "fedora", "macos", "linux"]
---

If you're a developer, you've probably experienced it: setting up a new machine is painful. Your aliases, configurations, keybindings, favorite tools — everything you spent years perfecting lives scattered across `.bashrc`, `.zshrc`, `.vimrc`, and dozens of other config files. And when you get a new work laptop or reinstall your OS? Start from scratch.

I've been there. After years of manually copying configs between machines, I decided to finally solve this properly. This is the story of how I built a **fully automated, cross-platform dotfiles system** using [chezmoi](https://www.chezmoi.io/) that handles everything from my shell aliases to my Neovim config to my terminal emulators — across macOS, Fedora (both regular and Atomic), Raspberry Pi, and Windows.

### Why Chezmoi?

Before diving into the solution, let's talk about why I chose chezmoi over other options:

| Tool | Pros | Cons |
|------|------|------|
| **GNU Stow** | Simple, lightweight | No templating, no scripts |
| **Yadm** | Good encryption support | Less active development |
| **Dotfiles symlinks** | Simple | Manual, error-prone |
| **Ansible** | Powerful, declarative | Overkill for dotfiles |
| **Chezmoi** | Templates, scripts, encryption, active dev | Learning curve |

Chezmoi hit the sweet spot: it treats your dotfiles as code, supports Go templates for conditional configuration, runs scripts during apply, encrypts secrets, and integrates seamlessly with Git. Plus, it's actively developed and has a great community.

### The Architecture

My dotfiles setup consists of several key components:

```
~/.local/share/chezmoi/
├── .chezmoiscripts/        # Automation scripts
│   ├── 01-setup/           # System prerequisites
│   ├── 02-install/         # Package installation
│   ├── 03-configure/       # Post-install config
│   └── 04-update/          # Update scripts
├── dot_config/             # XDG config files
├── dot_zsh/                # Zsh configuration (modular)
├── dot_bash/               # Bash configuration
├── scripts/                # Bootstrap scripts
└── .chezmoi.toml.tmpl      # Configuration template
```

### 1. Profile-Based Configuration

One of chezmoi's most powerful features is templating. I use this to apply different configurations based on machine type:

```toml
[data]
profile = "mac"        # or "linux", "windows", "rpi"
```

This allows me to have:
- **macOS**: Homebrew packages, specific aliases, Apple-friendly prompts
- **Fedora**: DNF packages, Flatpak for GUI apps, different prompt
- **Fedora Atomic**: Immutable OS considerations, rpm-ostree base layer
- **Raspberry Pi**: APT packages, lighter configuration
- **Windows**: Scoop packages, minimal bash config

### 2. Modular Shell Configuration

Instead of one giant `.zshrc`, I split my shell config into numbered files:

```
dot_zsh/
├── 00-env.zsh       # Environment variables
├── 01-path.zsh      # PATH management
├── 02-completions.zsh
├── 10-aliases.zsh   # Command aliases
├── 20-functions.zsh # Custom functions
├── 30-keybindings.zsh
└── 99-integrations.zsh  # FZF, Atuin, etc.
```

This makes finding and editing specific parts trivial. Need to add an alias? It's in `10-aliases.zsh`.

### 3. The Bootstrap Script: One-Command Setup

The centerpiece of my setup is a bootstrap script that:

1. **Detects the platform** (macOS, Fedora, Fedora Atomic, RPi, Debian, Windows)
2. **Installs prerequisites** (git, package manager)
3. **Installs chezmoi**
4. **Applies all dotfiles**
5. **Runs platform-specific setup scripts**

```bash
# One command to rule them all
curl -sL https://raw.githubusercontent.com/jsoyer/dotfiles/main/scripts/bootstrap.sh | bash
```

The script handles:
- **Fedora Atomic**: Special handling for rpm-ostree, base layer packages
- **SSH server**: Installation and enablement
- **Modern CLI tools**: eza, bat, ripgrep, etc.
- **chezmoi initialization**: Handles both fresh installs and updates

### 4. Automation Scripts

Chezmoi scripts are a game-changer. I have scripts that run:

- **Before apply** (`01-setup/`): Install system prerequisites
- **During apply** (`02-install/`): Install packages
- **After apply** (`03-configure/`): Configure things that need dotfiles first
- **On change** (`04-update/`): Update packages when dotfiles change

Example: On Fedora, the setup script detects whether it's regular Fedora, Fedora Atomic, or running in a Toolbox container, and adjusts package installation accordingly.

### 5. Auto-Sync: No More Manual Git Commands

The killer feature: I enabled auto-commit and auto-push in chezmoi:

```toml
[git]
autoAdd = true
autoCommit = true
autoPush = true
```

Now when I change a config:

```bash
# Edit directly in my home directory
nvim ~/.config/alacritty/alacritty.toml

# Re-add to chezmoi
chezmoi re-add ~/.config/alacritty/alacritty.toml

# Done! Auto-committed and pushed to GitHub
```

No manual `git add .`, `git commit`, `git push`. It's magical.

### 6. Secrets Management

For sensitive data (GPG keys, API tokens), I use chezmoi's encryption:

```bash
chezmoi add --encrypt ~/.zsh/secrets.zsh
```

Encrypted with a passphrase, decrypted automatically on new machines.

### The Daily Workflow

**On my main machine (MacBook Pro):**
1. Edit config files directly
2. Test changes
3. Run `chezmoi re-add <file>` — auto-commits and pushes

**On secondary machines:**
1. Run `chezmoi update` or `chezmoi apply`
2. Everything syncs automatically

**Updating packages:**
I have a `cup` alias (chezmoi update + package updates) that handles everything:
- chezmoi update
- Homebrew/DNF/Scoop upgrades
- Docker container updates

### Lessons Learned

1. **Start simple**: Don't try to migrate everything at once. Add files incrementally.

2. **Use templates wisely**: Conditional logic is powerful but can get complex. Document your templates.

3. **Test on VMs**: Before applying changes to your main machine, test on a VM or container.

4. **Bootstrap is key**: A good bootstrap script makes onboarding new machines trivial.

5. **Git is your friend**: The git working tree inside chezmoi gives you rollback capability.

### The Result

Now when I get a new machine:

```bash
# 5 minutes later, I'm productive
curl -sL https://raw.githubusercontent.com/jsoyer/dotfiles/main/scripts/bootstrap.sh | bash
```

My entire development environment — shell, editor, terminal, tools, aliases, functions — is exactly the same across:
- 💻 macOS (MacBook Pro, Mac Mini)
- 🐧 Fedora (desktop, laptop, Fedora Atomic on Framework)
- 🍓 Raspberry Pi
- 🪟 Windows (WSL)

**That's the power of treating your dotfiles as code.**

---

*Written with ❤️ using chezmoi-managed Neovim configuration*
