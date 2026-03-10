---
title: "chezmoi vs yadm vs stow : lequel choisir en 2025 ?"
date: 2025-09-03T09:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "Une comparaison pratique des trois gestionnaires de dotfiles les plus populaires — avec de vrais compromis, pas juste des tableaux de fonctionnalités."
categories: ["DevOps", "Tooling"]
tags: ["chezmoi", "dotfiles", "yadm", "stow", "automation", "linux", "macos"]
cover:
  image: /images/covers/chezmoi-vs-alternatives.webp
  alt: "chezmoi vs yadm vs stow"
---

J'ai utilisé les trois. J'ai choisi chezmoi. Mais la vraie réponse est : *ça dépend de ce que vous voulez faire*. Voici le bilan pratique, basé sur une utilisation réelle sur macOS, Fedora, Fedora Atomic, et Raspberry Pi.

> Vous connaissez déjà chezmoi ? Voir [mon setup complet ici](/posts/dotfiles/).

---

### Le problème à résoudre

Les dotfiles sont les fichiers de config qui vivent dans votre répertoire personnel : `.zshrc`, `.gitconfig`, `~/.config/nvim/`, etc. Le problème :

1. Ils sont dispersés dans votre système de fichiers
2. Vous voulez les versionner
3. Vous voulez les synchroniser entre plusieurs machines
4. Certaines valeurs diffèrent selon la machine (laptop pro vs perso, macOS vs Linux)
5. Certains fichiers contiennent des secrets qui ne doivent pas être dans Git

Chaque gestionnaire de dotfiles résout facilement les problèmes 1 et 2. Les problèmes 3, 4 et 5 sont là où ils divergent.

---

### GNU Stow

**L'approche :** des symlinks. Stow crée des symlinks d'un répertoire géré (`~/dotfiles/`) vers votre répertoire personnel.

```bash
# Structure
~/dotfiles/
  zsh/.zshrc           → ~/.zshrc
  nvim/.config/nvim/   → ~/.config/nvim/

# Appliquer
stow zsh
stow nvim
```

**Ce qu'il fait bien :**
- Conceptuellement simple — vous comprenez exactement ce qu'il fait
- Pas de magie, pas de format spécial
- Les fichiers sont de vrais fichiers dans un dépôt Git
- Fonctionne sur tout ce qui a un shell POSIX

**Ses limites :**
- Pas de templating — même fichier sur toutes les machines
- Pas de gestion des secrets
- Pas de scripts de setup
- La gestion de l'arbre de symlinks devient complexe avec des configs avancées

**Pour qui :** une seule machine, ou plusieurs machines identiques.

---

### yadm (Yet Another Dotfiles Manager)

**L'approche :** un wrapper Git. yadm traite votre répertoire personnel comme un dépôt Git, avec support des alternates (fichiers spécifiques à une machine) et du chiffrement.

```bash
yadm init
yadm add ~/.zshrc ~/.gitconfig
yadm commit -m "initial"
yadm push
```

**Ce qu'il fait bien :**
- Courbe d'apprentissage quasi nulle si vous connaissez Git
- Alternates : `~/.zshrc##os.Darwin` vs `~/.zshrc##os.Linux`
- Chiffrement intégré via GPG
- Scripts de bootstrap via `~/.config/yadm/bootstrap`

**Ses limites :**
- Les alternates sont basés sur les noms de fichiers, ce qui devient lourd avec beaucoup de variations
- Développement moins actif (dernière release majeure en 2023)
- Pas de templating natif (support Jinja2 ajouté mais bricolé)

**Pour qui :** un développeur solo qui veut une gestion Git native des dotfiles avec un minimum de nouveaux outils.

---

### chezmoi

**L'approche :** une machine à états dédiée. chezmoi gère un répertoire source (`~/.local/share/chezmoi/`) et l'applique à votre répertoire personnel.

```bash
chezmoi add ~/.zshrc
chezmoi edit ~/.zshrc   # édite la source, pas le fichier live
chezmoi apply           # applique les changements
chezmoi diff            # montre ce qui changerait
```

**Ce qu'il fait bien :**
- Templates Go : un seul fichier, contenu différent par machine
- Scripts : s'exécutent au premier apply, au changement, ou à chaque fois
- Plusieurs backends de chiffrement (GPG, age, 1Password, Bitwarden)
- Fichiers externes : récupère des dotfiles depuis des URLs ou des dépôts Git
- `chezmoi diff` avant d'appliquer — vous voyez toujours ce qui va changer
- Développement actif, communauté solide

**Ses limites :**
- Courbe d'apprentissage : les conventions de nommage du répertoire source prennent du temps à assimiler (`dot_`, `executable_`, `private_`, `.tmpl`)
- Nouveau modèle mental — éditer `~/.zshrc` ne change pas automatiquement la source chezmoi (il faut `chezmoi re-add`)
- Overkill pour une seule machine

**Pour qui :** setups multi-machines, multi-OS.

---

### Comparaison côte à côte

| Fonctionnalité | Stow | yadm | chezmoi |
|----------------|------|------|---------|
| **Approche** | Symlinks | Wrapper Git | Machine à états |
| **Templating** | Non | Limité (Jinja2) | Oui (Go templates) |
| **Scripts de setup** | Non | Oui (bootstrap) | Oui (.chezmoiscripts) |
| **Chiffrement** | Non | Oui (GPG) | Oui (GPG, age, 1Password...) |
| **Support multi-OS** | Manuel | Alternates (filename) | Templates (logique conditionnelle) |
| **Courbe d'apprentissage** | Faible | Faible-Moyen | Moyen |
| **Développement actif** | Stable/maintenu | Plus lent | Très actif |
| **Sources externes** | Non | Non | Oui |
| **Auto-commit/push** | Non | Via Git | Oui (intégré) |

---

### Mon choix : chezmoi

Je fais tourner les mêmes dotfiles sur 5+ machines sous 4 OS. Le système de templates est décisif :

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

Un seul fichier. Fonctionne partout. L'alternative avec Stow serait de maintenir 4 `.zshrc` séparés et de les synchroniser manuellement. Avec yadm, j'aurais 4 alternates et dupliquerais quand même la majorité du contenu.

L'auto-commit/push est aussi une fonctionnalité décisive au quotidien — je fais `chezmoi re-add` et mes changements sont dans Git, poussés sur GitHub, prêts pour mes autres machines.

---

### Guide de décision rapide

```
Une machine ? → Stow (simple) ou yadm (natif Git)
Plusieurs machines, même OS ? → yadm
Plusieurs machines, plusieurs OS ? → chezmoi
Besoin de gérer des secrets ? → chezmoi ou yadm
Zéro nouveau modèle mental ? → yadm
Puissance maximale ? → chezmoi
```

> **Plongée complète :** [Dotfiles Revolution : Mon setup chezmoi complet](/fr/posts/dotfiles/) couvre l'implémentation totale — templates, scripts, intégration 1Password, et configuration multi-plateforme.

---

*Voir [mon setup chezmoi complet](/posts/dotfiles/) pour l'implémentation détaillée*
