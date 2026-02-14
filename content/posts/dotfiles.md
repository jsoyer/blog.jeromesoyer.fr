---
title: "Dotfiles Revolution: How I Manage My Entire dev Environment with Chezmoi"
date: 2026-02-14T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "A comprehensive guide to cross-platform dotfiles management"
categories: ["DevOps", "Linux", "macOS"]
tags: ["chezmoi", "dotfiles", "automation", "fedora", "macos", "linux"]
---

# [EN] Dotfiles Revolution: How I Manage My Entire dev Environment with Chezmoi

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

# [FR] Dotfiles Revolution : Comment je gère tout mon environnement de dev avec Chezmoi

### Le Problème : Chaque Machine est Unique

Si vous êtes développeur, vous l'avez probablement vécu : configurer une nouvelle machine est douloureux. Vos alias, configurations, raccourcis clavier, outils préférés — tout ce sur quoi vous avez passé des années à peaufiner — est dispersé à travers `.bashrc`, `.zshrc`, `.vimrc`, et des dizaines d'autres fichiers de config. Et quand vous avez un nouvel ordinateur ou réinstallez votre OS ? Tout recommencer à zéro.

J'ai été là. Après des années à copier manuellement des configs entre machines, j'ai décidé de résoudre ce problème définitivement. Voici l'histoire de comment j'ai construit un **système de dotfiles entièrement automatisé et multi-plateforme** utilisant [chezmoi](https://www.chezmoi.io/) qui gère tout : de mes alias shell à ma config Neovim en passant par mes émulateurs de terminal — sur macOS, Fedora (classique et Atomic), Raspberry Pi, et Windows.

### Pourquoi Chezmoi ?

Avant de parler de la solution, parlons de pourquoi j'ai choisi chezmoi plutôt que d'autres options :

| Outil | Avantages | Inconvénients |
|-------|-----------|---------------|
| **GNU Stow** | Simple, léger | Pas de templating, pas de scripts |
| **Yadm** | Bon support du chiffrement | Développement moins actif |
| **Dotfiles symlinks** | Simple | Manuel, sujet aux erreurs |
| **Ansible** | Puissant, déclaratif | Trop lourd pour des dotfiles |
| **Chezmoi** | Templates, scripts, chiffrement, développement actif | Courbe d'apprentissage |

Chezmoi a trouvé le juste milieu : il traite vos dotfiles comme du code, supporte les templates Go pour la configuration conditionnelle, exécute des scripts pendant l'application, chiffre les secrets et s'intègre parfaitement avec Git. De plus, il est activement développé et a une communauté formidable.

### L'Architecture

Mon système de dotfiles se compose de plusieurs composants clés :

```
~/.local/share/chezmoi/
├── .chezmoiscripts/        # Scripts d'automatisation
│   ├── 01-setup/           # Prérequis système
│   ├── 02-install/         # Installation de paquets
│   ├── 03-configure/       # Configuration post-install
│   └── 04-update/          # Scripts de mise à jour
├── dot_config/             # Fichiers de config XDG
├── dot_zsh/                # Configuration Zsh (modulaire)
├── dot_bash/               # Configuration Bash
├── scripts/                # Scripts de bootstrap
└── .chezmoi.toml.tmpl      # Modèle de configuration
```

### 1. Configuration Basée sur le Profil

Une des fonctionnalités les plus puissantes de chezmoi est le templating. Je l'utilise pour appliquer différentes configurations selon le type de machine :

```toml
[data]
profile = "mac"        # ou "linux", "windows", "rpi"
```

Cela me permet d'avoir :
- **macOS** : Paquets Homebrew, alias spécifiques, prompts adaptés à Apple
- **Fedora** : Paquets DNF, Flatpak pour les apps GUI, prompt différent
- **Fedora Atomic** : Considérations pour OS immuable, couche de base rpm-ostree
- **Raspberry Pi** : Paquets APT, configuration légère
- **Windows** : Paquets Scoop, config bash minimale

### 2. Configuration Shell Modulaire

Au lieu d'un `.zshrc` géant, je divise ma config shell en fichiers numérotés :

```
dot_zsh/
├── 00-env.zsh       # Variables d'environnement
├── 01-path.zsh      # Gestion du PATH
├── 02-completions.zsh
├── 10-aliases.zsh   # Alias de commandes
├── 20-functions.zsh # Fonctions personnalisées
├── 30-keybindings.zsh
└── 99-integrations.zsh  # FZF, Atuin, etc.
```

Trouver et éditer des parties spécifiques devient trivial. Besoin d'ajouter un alias ? C'est dans `10-aliases.zsh`.

### 3. Le Script de Bootstrap : Configuration en Une Commande

Le cœur de ma configuration est un script de bootstrap qui :

1. **Détecte la plateforme** (macOS, Fedora, Fedora Atomic, RPi, Debian, Windows)
2. **Installe les prérequis** (git, gestionnaire de paquets)
3. **Installe chezmoi**
4. **Applique tous les dotfiles**
5. **Exécute les scripts de configuration spécifiques à la plateforme**

```bash
# Une commande pour tout configurer
curl -sL https://raw.githubusercontent.com/jsoyer/dotfiles/main/scripts/bootstrap.sh | bash
```

Le script gère :
- **Fedora Atomic** : Traitement spécial pour rpm-ostree, couche de base
- **Serveur SSH** : Installation et activation
- **Outils CLI modernes** : eza, bat, ripgrep, etc.
- **Initialisation chezmoi** : Gère les nouvelles installs et les mises à jour

### 4. Scripts d'Automatisation

Les scripts chezmoi sont révolutionnaires. J'ai des scripts qui s'exécutent :

- **Avant l'application** (`01-setup/`) : Installer les prérequis système
- **Pendant l'application** (`02-install/`) : Installer les paquets
- **Après l'application** (`03-configure/`) : Configurer les choses qui ont besoin des dotfiles
- **Au changement** (`04-update/`) : Mettre à jour les paquets quand les dotfiles changent

Exemple : Sur Fedora, le script de setup détecte si c'est Fedora classique, Fedora Atomic, ou si ça tourne dans un Toolbox, et ajuste l'installation des paquets en conséquence.

### 5. Auto-Sync : Plus de Commandes Git Manuelles

La fonctionnalité décisive : j'ai activé auto-commit et auto-push dans chezmoi :

```toml
[git]
autoAdd = true
autoCommit = true
autoPush = true
```

Maintenant quand je change une config :

```bash
# Éditer directement dans mon répertoire personnel
nvim ~/.config/alacritty/alacritty.toml

# Re-ajouter à chezmoi
chezmoi re-add ~/.config/alacritty/alacritty.toml

# C'est fait ! Auto-commit et push vers GitHub
```

Plus de `git add .`, `git commit`, `git push` manuels. C'est magique.

### 6. Gestion des Secrets

Pour les données sensibles (clés GPG, tokens API), j'utilise le chiffrement de chezmoi :

```bash
chezmoi add --encrypt ~/.zsh/secrets.zsh
```

Chiffré avec une phrase de passe, déchiffré automatiquement sur les nouvelles machines.

### Le Quotidien

**Sur ma machine principale (MacBook Pro) :**
1. Éditer les fichiers de config directement
2. Tester les changements
3. Lancer `chezmoi re-add <fichier>` — auto-commit et push

**Sur les machines secondaires :**
1. Lancer `chezmoi update` ou `chezmoi apply`
2. Tout se synchronise automatiquement

**Mettre à jour les paquets :**
J'ai un alias `cup` (chezmoi update + mise à jour des paquets) qui gère tout :
- chezmoi update
- Mises à jour Homebrew/DNF/Scoop
- Mises à jour des containers Docker

### Leçons Apprises

1. **Commencer simple** : N'essayez pas de tout migrer d'un coup. Ajoutez les fichiers progressivement.

2. **Utiliser le templating intelligemment** : La logique conditionnelle est puissante mais peut devenir complexe. Documentez vos templates.

3. **Tester sur VMs** : Avant d'appliquer des changements sur votre machine principale, testez sur une VM ou un container.

4. **Le bootstrap est clé** : Un bon script de bootstrap rend l'onboarding de nouvelles machines trivial.

5. **Git est votre ami** : L'arbre de travail git à l'intérieur de chezmoi vous donne la capacité de revenir en arrière.

### Le Résultat

Maintenant quand j'ai une nouvelle machine :

```bash
# 5 minutes plus tard, je suis productif
curl -sL https://raw.githubusercontent.com/jsoyer/dotfiles/main/scripts/bootstrap.sh | bash
```

Mon environnement de développement complet — shell, éditeur, terminal, outils, alias, fonctions — est exactement le même sur :
- 💻 macOS (MacBook Pro, Mac Mini)
- 🐧 Fedora (bureau, laptop, Fedora Atomic sur Framework)
- 🍓 Raspberry Pi
- 🪟 Windows (WSL)

**C'est le pouvoir de traiter ses dotfiles comme du code.**

---

*Written with ❤️ using chezmoi-managed Neovim configuration*

*Écrit avec ❤️ en utilisant une configuration Neovim gérée par chezmoi*
