---
title: "Framework Laptop + Fedora Atomic : le cas pour un OS immuable"
date: 2026-03-09T23:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "Pourquoi les distributions Linux immuables comptent. Faire tourner Fedora Atomic sur Framework pour stabilité et flexibilité."
categories: ["Linux", "Tooling"]
tags: ["fedora", "linux", "framework", "immutable-os", "flatpak", "dotfiles", "productivité"]
cover:
  image: /images/covers/framework-fedora-atomic.webp
  alt: "Framework Laptop Fedora Atomic"
---

J'ai été utilisateur Linux desktop pendant des années, mais j'ai toujours eu l'impression de jouer avec le feu. Installez un package mal, allez bousiller un fichier de config, et soudainement vous debuggez un système cassé à 2 du matin. Chaque laptop de dev finit par devenir un Frankenstein d'outils demi-installés et de dépendances conflictuelles.

Ensuite j'ai découvert Fedora Atomic (maintenant appelé Fedora Silverblue et Kinoite), et ça a fondamentalement changé comment je pense aux systèmes d'exploitation.

## Le problème avec Linux traditionnel

Les distributions Linux traditionnelles vous laissent modifier n'importe quoi. Vous avez l'accès root, vous pouvez installer des packages globalement, vous pouvez éditer les fichiers système. C'est puissant — et dangereux.

Le problème : après 18 mois de développement, votre `/usr/lib` est plein de packages orphelins, votre démarrage shell prend 5 secondes à cause d'hooks accumulés, et vous n'avez aucune idée pourquoi PostgreSQL ne démarre pas à cause de quelque changement de config que vous avez fait il y a un an et oublié.

La solution conventionnelle c'est juste de reconstruire votre système de zéro chaque an ou deux. Pas idéal.

## OS immuable : une philosophie différente

Fedora Atomic flip le script : le filesystem OS (`/usr`, `/etc` pour la plupart) est read-only. Vous ne modifiez pas le système de base ; au lieu de ça, vous composez des changements par-dessus.

Les concepts clefs :

**rpm-ostree** : Gère votre image OS atomiquement. Les upgrades, layers, et rollbacks se passent comme des transactions atomiques.

```bash
# Upgradez l'image d'OS entière
rpm-ostree upgrade

# Quelque chose a cassé ? Rollback vers l'image précédente
rpm-ostree rollback

# Reboot si nécessaire (généralement automatique)
systemctl reboot
```

**Layers** : Si vous avez besoin de packages système, vous les layerez par-dessus :

```bash
# Ajoutez Neovim, Zsh, Kitty à votre layer OS
rpm-ostree install neovim zsh kitty
```

Ces changements sont permanents (jusqu'à ce que vous les retiriez) et s'upgradent comme partie du prochain `upgrade`.

**toolbox/distrobox** : Pour les outils de dev et les trucs spécifiques à un langage (Node, Python, Rust, etc.), vous utilisez des containers au lieu de polluer l'OS de base :

```bash
# Créez un container de développement avec Node.js
toolbox create --container dev-tools
toolbox run --container dev-tools npm --version

# Fonctionne de manière transparente depuis votre shell host
```

Le container a accès à votre home directory et fichiers, mais c'est isolé de l'OS de base. Vous pouvez le nuker et le recréer en secondes.

## Fedora Atomic sur Framework : une paire parfaite

Les Framework Laptops sont construits pour la flexibilité — design modulaire, firmware ouvert, aucune propriétaire nonsense. Fedora Atomic c'est l'OS qui match cette philosophie.

Mon setup sur Framework :

```bash
# Layer système de base
rpm-ostree install \
  vim zsh \
  git \
  htop neofetch \
  podman \
  tailscale

# Outils de dev dans containers (pas de pollution host)
toolbox create --container rust-dev
toolbox run -c rust-dev sudo dnf install rustup cargo rust-analyzer

toolbox create --container node-dev
toolbox run -c node-dev sudo dnf install npm nodejs
```

L'OS de base reste clean. Les outils de dev vivent dans des containers. Quand je change de projet, j'active juste le bon container.

## Dotfiles : une config, deux machines

J'utilise chezmoi pour gérer mes dotfiles sur macOS et Fedora Atomic. La clé c'est le templating :

```toml
# ~/.config/mise/config.toml (managé par template chezmoi)
[tools]
node = "{{ .node_version }}"
python = "{{ .python_version }}"

{{ if eq .chezmoi.os "darwin" }}
# Config spécifique macOS
[terminals.iterm2]
enabled = true
{{ else if eq .chezmoi.osRelease.id "fedora" }}
# Config Fedora Atomic
[terminals.kitty]
enabled = true
{{ end }}
```

Le `.chezmoi.toml.tmpl` définit les variables :

```toml
[node_version]
node_version = "22"
python_version = "3.12"
```

Lancer `chezmoi apply` sur n'importe quelle machine génère la bonne config. Mon shell config, les settings d'éditeur, et la configuration d'outils sont identiques — juste avec les overrides spécifiques à la plateforme baked in.

## L'expérience réelle

**Ce qui marche magnifiquement :**

- Fedora Atomic c'est *boring*. Vous installez une fois, les layers restent clean, les upgrades sont atomiques (pas d'états demi-cassés)
- Flatpaks (apps containerisées) évitent l'enfer des dépendances pour les apps GUI
- Rollback depuis un upgrade cassé c'est une commande
- La base immuable veut dire que vous ne pouvez pas accidentellement casser votre OS en messant avec les fichiers de config

**Ce qui est un peu awkward :**

- Certains outils ne sont pas disponibles comme Flatpaks (Slack vient à peine d'en avoir un, certains outils de niche n'existent pas)
- Les layers de packages système doivent quand même être managés (pas tous les outils fonctionnent dans les containers)
- La courbe d'apprentissage : penser en "layers + containers" au lieu de "just install it globally" demande d'ajustement

## Le dividende de stabilité

Après 18 mois sur Framework + Fedora Atomic, mon système est toujours rapide et stable. Pas de dépendances Frankenstein, pas d'upgrades demi-cassés, pas de fichiers système mystérieux que je ne reconnais pas.

C'est la promesse des OS immuables : *stabilité sans stagnation*. Vous obtenez des upgrades atomiques et rollbacks (fiabilité) avec accès aux packages les plus récents (fraîcheur).

## C'est pour tout le monde ?

Non. Si vous êtes utilisateur Windows, ça ne vous appellera pas. Si vous utilisez Linux mais détestez les containers et préférez un modèle plus simple, restez sur Ubuntu ou Fedora Workstation.

Mais si vous êtes un développeur qui veut un setup Linux rock-solid qui reste clean avec le temps, sans l'overhead de gérer une distro traditionnelle, Fedora Atomic vaut d'être essayé. Appairez-le avec Framework (hardware que vous contrôlez), managez vos dotfiles avec chezmoi (config que vous contrôlez), et vous obtenez un setup qui est à la fois puissant et maintenable.

L'avenir des OS desktops pourrait être immuable. Vaut d'explorer maintenant.
