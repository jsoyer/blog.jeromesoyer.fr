---
title: "Framework Laptop + Fedora Atomic: The Case for an Immutable OS"
date: 2026-03-09T23:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Why immutable Linux distributions matter. Running Fedora Atomic on a Framework laptop for maximum stability and flexibility."
categories: ["Linux", "Tooling"]
tags: ["fedora", "linux", "framework", "immutable-os", "flatpak", "dotfiles", "productivity"]
cover:
  image: /images/covers/framework-fedora-atomic.webp
  alt: "Framework Laptop Fedora Atomic"
---

I've been a Linux desktop user for years, but I've always felt like I was playing with fire. Install a package wrong, mess up a config file, and suddenly you're debugging a broken system at 2 AM. Every dev laptop eventually becomes a Frankenstein of half-installed tools and conflicting dependencies.

Then I discovered Fedora Atomic (now called Fedora Silverblue and Kinoite), and it fundamentally changed how I think about operating systems.

## The Problem with Traditional Linux

Traditional Linux distributions let you modify anything. You have root access, you can install packages globally, you can edit system files. This is powerful—and dangerous.

The problem: after 18 months of development, your `/usr/lib` is full of orphaned packages, your shell startup takes 5 seconds because of accumulated hooks, and you have no idea why PostgreSQL won't start because of some config change you made a year ago and forgot about.

The conventional solution is to just rebuild your system from scratch every year or so. Not ideal.

## Immutable OS: A Different Philosophy

Fedora Atomic flips the script: the OS filesystem (`/usr`, `/etc` for most things) is read-only. You don't modify the base system; instead, you compose changes on top of it.

The key concepts:

**rpm-ostree**: Manages your OS image atomically. Upgrades, layers, and rollbacks happen as atomic transactions.

```bash
# Update the entire OS image
rpm-ostree upgrade

# Something broke? Rollback to previous image
rpm-ostree rollback

# Reboot if needed (usually automatic)
systemctl reboot
```

**Layers**: If you need system packages, you layer them on top:

```bash
# Add Neovim, Zsh, Kitty to your OS layer
rpm-ostree install neovim zsh kitty
```

These changes are permanent (until you remove them) and update as part of the next `upgrade`.

**toolbox/distrobox**: For development tools and language-specific stuff (Node, Python, Rust, etc.), you use containers instead of polluting the base OS:

```bash
# Create a development container with Node.js
toolbox create --container dev-tools
toolbox run --container dev-tools npm --version

# Works seamlessly from your host shell
```

The container has access to your home directory and files, but it's isolated from the base OS. You can nuke it and recreate it in seconds.

## Fedora Atomic on Framework: A Perfect Pair

Framework Laptops are built for flexibility—modular design, open firmware, no proprietary nonsense. Fedora Atomic is the OS that matches that philosophy.

My setup on Framework:

```bash
# Base system layer
rpm-ostree install \
  vim zsh \
  git \
  htop neofetch \
  podman \
  tailscale

# Dev tools in containers (no host pollution)
toolbox create --container rust-dev
toolbox run -c rust-dev sudo dnf install rustup cargo rust-analyzer

toolbox create --container node-dev
toolbox run -c node-dev sudo dnf install npm nodejs
```

The base OS stays clean. Dev tools live in containers. When I switch projects, I just activate the right container.

## Dotfiles: One Config, Two Machines

I use chezmoi to manage my dotfiles across macOS and Fedora Atomic. The key is templating:

```toml
# ~/.config/mise/config.toml (managed by chezmoi template)
[tools]
node = "{{ .node_version }}"
python = "{{ .python_version }}"

{{ if eq .chezmoi.os "darwin" }}
# macOS-specific config
[terminals.iterm2]
enabled = true
{{ else if eq .chezmoi.osRelease.id "fedora" }}
# Fedora Atomic config
[terminals.kitty]
enabled = true
{{ end }}
```

The `.chezmoi.toml.tmpl` defines variables:

```toml
[node_version]
node_version = "22"
python_version = "3.12"
```

Running `chezmoi apply` on either machine generates the right config. My shell config, editor settings, and tool configuration are identical—just with platform-specific overrides baked in.

## The Real-World Experience

**What works beautifully:**

- Fedora Atomic is *boring*. You install it once, layers stay clean, upgrades are atomic (no half-broken states)
- Flatpaks (containerized apps) avoid dependency hell for GUI apps
- Rolling back from a broken upgrade is one command
- The immutable base means you can't accidentally break your OS by messing with config files

**What's a bit awkward:**

- Some tools aren't available as Flatpaks yet (Slack just barely got one, some niche tools don't exist)
- System package layers still need to be managed (not all tools work in containers)
- The learning curve: thinking in "layers + containers" instead of "just install it globally" takes adjustment

## The Stability Dividend

After 18 months on Framework + Fedora Atomic, my system is still fast and stable. No Frankenstein dependencies, no half-broken upgrades, no mystery system files I don't recognize.

This is the promise of immutable OSes: *stability without stagnation*. You get atomic upgrades and rollbacks (reliability) with access to the latest packages (freshness).

## Is This For Everyone?

No. If you're a Windows user, this won't appeal to you. If you use Linux but hate containers and prefer a simpler model, stick with Ubuntu or Fedora Workstation.

But if you're a developer who wants a rock-solid Linux setup that stays clean over time, without the overhead of managing a traditional distro, Fedora Atomic is worth trying. Pair it with Framework (hardware you control), manage your dotfiles with chezmoi (config you control), and you get a setup that's both powerful and maintainable.

The future of desktop OSes might be immutable. Worth exploring now.
