---
title: "Kitty Terminal : Plongée dans la bête GPU-accélérée"
date: 2025-08-20T11:45:00+02:00
draft: false
author: "Jerome Soyer"
description: "Au-delà des onglets — les kittens, les layouts, le scripting, et pourquoi c'est mon terminal principal depuis des années."
categories: ["Tooling", "Terminal"]
tags: ["kitty", "terminal", "productivity", "gpu", "cli", "automation"]
cover:
  image: /images/covers/kitty-deep-dive.webp
  alt: "Kitty Terminal Deep Dive"
---

La plupart des développeurs choisissent leur terminal comme ils choisissent une police : une fois, un peu au hasard, et ils ne changent plus jamais. J'étais pareil — jusqu'à ce que j'essaie **[Kitty](https://sw.kovidgoyal.net/kitty/)** et réalise que je laissais des performances et des fonctionnalités sur la table depuis des années.

### Pourquoi Kitty ?

Le pitch est simple : rendu GPU-accéléré, scriptable en Python, et un concept appelé **kittens** (petits programmes terminaux qui étendent les fonctionnalités). Rapide, programmable, et qui ne s'impose pas.

### Les Layouts : le super-pouvoir méconnu

Kitty a un système de tiling intégré. Sans tmux.

```ini
enabled_layouts tall, fat, grid, horizontal, vertical, stack
```

Cycling avec `ctrl+shift+l`. Mon préféré : **tall** — un panneau principal à gauche, une pile de petits panneaux à droite.

### Le Contrôle à Distance : scriptez tout

```ini
# kitty.conf
allow_remote_control yes
listen_on unix:/tmp/kitty
```

Depuis n'importe quel script :

```bash
# Ouvrir un nouvel onglet nommé "logs"
kitty @ new-window --title logs --type tab

# Envoyer une commande à une fenêtre spécifique
kitty @ send-text --match title:logs "tail -f /var/log/app.log\n"
```

C'est la base de mon [extension Raycast Kitty](/posts/raycast-kitty/) — tout passe par des commandes `kitty @`.

### Les Launch Configs YAML

Définissez des layouts complets en YAML, lancez en une commande. Mon environnement de dev complet — éditeur, serveur, logs — s'ouvre parfaitement arrangé.

### Verdict

Si vous passez votre vie dans le terminal, Kitty vaut le passage. La courbe d'apprentissage est courte, le gain en vitesse et en scriptabilité est réel.

### Prochaines étapes

- **Configurer l'éditeur :** [Mon setup Neovim en 2025](/fr/posts/neovim-setup/) — configurer Neovim pour fonctionner dans Kitty.
- **Automatiser avec Raycast :** [Extension Raycast Kitty](/fr/posts/raycast-kitty/) — recherche d'onglets, lancement de configs, tout depuis Raycast.

---

*Config complète disponible dans mes [dotfiles](https://github.com/jsoyer)*
