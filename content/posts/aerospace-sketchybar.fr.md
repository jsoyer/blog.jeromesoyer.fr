---
title: "Aerospace + Sketchybar : Mon setup macOS entièrement au clavier"
date: 2025-12-03T14:30:00+01:00
draft: false
author: "Jerome Soyer"
description: "Un gestionnaire de fenêtres en pavage + barre de menu scriptable pour une productivité macOS au clavier"
categories: ["macOS", "Tooling"]
tags: ["macos", "aerospace", "sketchybar", "automation", "productivite", "cli", "dotfiles"]
cover:
  image: /images/covers/aerospace-sketchybar.webp
  alt: "Setup Aerospace Sketchybar macOS"
---

J'utilise macOS depuis des années, mais une chose m'a toujours agacé : l'absence d'un véritable gestionnaire de fenêtres au clavier. Stage Manager ressemble à un jouet, Mission Control est chaotique, et l'alt+tab, c'est inefficace. Je passais beaucoup trop de temps à chercher la souris.

Puis j'ai découvert **Aerospace** — un gestionnaire de fenêtres en pavage (tiling) pour macOS, sans avoir à désactiver la protection du système. Combiné à **Sketchybar** (un remplaçant scriptable de la barre de menu macOS), j'ai créé un setup qui ressemble moins à macOS et plus à i3 ou Hyprland sous Linux. Sauf que ça marche de façon transparente sur mon MacBook Pro.

### Le problème : gestion des fenêtres sous macOS

La gestion native des fenêtres chez Apple, c'est décevant si tu es fan du clavier :
- **Mission Control** : Swipe vers le haut, chercher la petite preview, cliquer. 3 secondes par changement d'espace.
- **Stage Manager** : Ça ressemble à une barre latérale qui essaie trop fort.
- **Snap de fenêtres** : On peut snapper à demi-écran, mais c'est limité et maladroit.

Je travaille avec 4-5 fenêtres ouvertes en permanence — Neovim, navigateur, Slack, logs de debug, tests. Sans tiling, soit j'ai des fenêtres superposées (chiant à switcher), soit je change constamment les tailles. J'avais envie des **workspaces** et du **tiling** que les utilisateurs Linux ont par défaut.

### Voilà Aerospace

**Aerospace** est un gestionnaire de fenêtres en pavage léger écrit en Swift. Pas besoin de désactiver SIP. Pas de piratage du système. Juste un fichier de config et des raccourcis clavier.

**Installation :**
```bash
brew install nikitabobko/tap/aerospace
```

**Configuration de base** (`~/.aerospace.toml`) :
```toml
# Lancer au démarrage
start-at-login = true

[mode.main.binding]
# Focus des fenêtres (style vim hjkl)
alt-h = 'focus left'
alt-l = 'focus right'
alt-j = 'focus down'
alt-k = 'focus up'

# Déplacer des fenêtres
alt-shift-h = 'move left'
alt-shift-l = 'move right'
alt-shift-j = 'move down'
alt-shift-k = 'move up'

# Switcher de workspace (Alt + chiffre)
alt-1 = 'workspace 1'
alt-2 = 'workspace 2'
alt-3 = 'workspace 3'
alt-4 = 'workspace 4'
alt-5 = 'workspace 5'

# Déplacer fenêtre vers workspace
alt-shift-1 = 'move-node-to-workspace 1'
alt-shift-2 = 'move-node-to-workspace 2'

# Split et fullscreen
alt-e = 'layout tiles horizontal'
alt-o = 'layout tiles vertical'
alt-shift-e = 'layout accordion horizontal'
alt-shift-o = 'layout accordion vertical'
alt-shift-f = 'fullscreen'

# Fermer fenêtre
alt-w = 'close'
```

Ce que j'aime :
- **Isolation des workspaces** : Alt+3 me met sur l'espace 3 avec mes outils de debug. Alt+1, c'est mail/chat. Plus de mélange.
- **Touches modales** : Zéro collision avec les raccourcis des apps. `Alt-H` focus à gauche dans ma couche Aerospace, mais Vim récupère quand même son `H` pour l'historique.
- **Layouts** : Pavé (splits égaux), accordéon (empilé). Switcher avec une touche.
- **Pas de bloat** : C'est juste la gestion des fenêtres, pas un DE complet comme Yabai.

### Sketchybar : Le compagnon parfait

Aerospace marche bien, mais j'avais envie d'un **retour visuel** de quel workspace j'étais en train d'utiliser. C'est là que **Sketchybar** intervient.

Sketchybar remplace la barre de menu de macOS. C'est entièrement scriptable en Bash et Lua. Je l'utilise pour :
1. **Afficher le workspace actif d'Aerospace** (surligné dans ma barre de statut)
2. **Stats CPU/mémoire** (infos système en direct)
3. **Pourcentage batterie** (pour mon MacBook)
4. **Heure et date**
5. **Indicateur disposition clavier** (je switche entre EN/FR/BÉPO)

**Installation :**
```bash
brew install sketchybar
brew services start sketchybar
```

**Config Sketchybar de base** (`~/.config/sketchybar/sketchybarrc`) :
```bash
#!/bin/bash

# Palette de couleurs
export COLOR_BACKGROUND=0x1a1a1a
export COLOR_TEXT=0xffffff
export COLOR_ACCENT=0x61afef

# Indicateur de workspaces - affiche les workspaces Aerospace
for i in {1..9}; do
  sketchybar --add item workspace.$i left \
    --set workspace.$i \
    label=$i \
    width=35 \
    align=center \
    click-script="aerospace workspace $i"
done

# Stats système
sketchybar --add item cpu right \
  --set cpu update_freq=2 \
  --script '$PLUGIN_DIR/cpu.sh'

sketchybar --add item memory right \
  --set memory update_freq=2 \
  --script '$PLUGIN_DIR/memory.sh'

# Horloge
sketchybar --add item clock right \
  --set clock update_freq=10 \
  --script 'date "+%H:%M:%S"'
```

**Plugin pour syncer les workspaces Aerospace** (`$PLUGIN_DIR/aerospace_workspace.sh`) :
```bash
#!/bin/bash
# Récupère le workspace Aerospace actif via CLI aerospace
CURRENT=$(aerospace list-workspaces --focused)

for i in {1..9}; do
  if [ "$i" -eq "$CURRENT" ]; then
    sketchybar --set workspace.$i background.color=0x61afef
  else
    sketchybar --set workspace.$i background.color=0x1a1a1a
  fi
done
```

La magie : je clique un chiffre de workspace dans Sketchybar, ça exécute `aerospace workspace 5`. Ou j'appuie sur Alt+5. Les deux fonctionnent.

### Chezmoi : Version control pour les deux

Puisque mon setup s'étend sur macOS + Fedora + Raspberry Pi, je gère les configs Aerospace et Sketchybar dans **chezmoi** :

```
~/.local/share/chezmoi/
├── dot_aerospace/
│   └── aerospace.toml.tmpl
└── dot_config/sketchybar/
    ├── sketchybarrc.tmpl
    └── plugins/
        ├── cpu.sh
        ├── memory.sh
        └── aerospace_workspace.sh
```

Les fichiers `.tmpl` me permettent de personnaliser workspaces et bindings selon la machine :

```toml
# .aerospace.toml.tmpl
start-at-login = {{ if eq .chezmoi.os "darwin" }}true{{ else }}false{{ end }}

[mode.main.binding]
alt-h = 'focus left'
# Switcher de workspace - adapter le nombre selon la machine
{{- if eq .chezmoi.hostname "macbook-pro" }}
# Plus de workspaces sur la machine principale
alt-9 = 'workspace 9'
{{- end }}
```

Un `chezmoi apply` et les deux outils sont configurés de manière cohérente.

### Aerospace vs Yabai

Les gens demandent : pourquoi pas **Yabai** ? Yabai est plus puissant — scripting véritable, plus de contrôle. Mais Yabai oblige à **désactiver SIP**, ce que je ne suis pas à l'aise de faire sur mon MacBook professionnel (raisons de sécurité). Aerospace, ça marche sans pirater macOS. Compromis : moins de customization, mais tranquillité d'esprit.

### La sensation quotidienne

Quand je réveille mon MacBook :

```
Alt+1  → Slack + Mail (workspace 1)
Alt+2  → Navigateur + Recherche (workspace 2)
Alt+3  → Neovim + Tests + Logs (workspace 3, souvent split vertical)
Alt+4  → Appels Zoom (fullscreen)
```

Le switcher entre fenêtres, c'est :
```
Alt+H  → Focus fenêtre à gauche
Alt+J  → Focus fenêtre en dessous
Alt+Shift+L  → Déplacer fenêtre à droite
```

Pas de souris. Pas de Mission Control. Juste du clavier.

Sketchybar affiche les indicateurs de workspace en un coup d'œil, les stats système ne polluent pas le terminal, et tout se sent snappy.

### Leçons apprises

1. **Commencer avec des defaults sûrs** : Les defaults d'Aerospace sont solides. Tweak les bindings pour matcher ta mémoire musculaire (moi, j'utilise vim hjkl).

2. **Les plugins Sketchybar, c'est du bash** : Si tu sais écrire du bash, tu peux étendre ta barre de menu. Pas besoin d'apprendre Swift.

3. **Teste la config avant de redémarrer** : `aerospace reload` et `sketchybar --reload` attrapent les erreurs de syntaxe.

4. **Les templates chezmoi, c'est salvateur** : Si tu gères plusieurs machines, utilise des templates pour les nombres de workspaces, les noms, etc.

5. **Certaines apps ne jouent pas le jeu** : Zoom, Figma, certains IDEs ont un comportement weird en pavage. Tu peux les laisser flotter :
   ```toml
   [[on-window-detected]]
   if.app-id = 'us.zoom.xos'
   then = ['layout floating']
   ```

### Le verdict

Aerospace + Sketchybar ont transformé mon expérience macOS. Je suis plus rapide, je touche beaucoup moins à la souris, et mon setup se sent **intentionnel** plutôt que réactif. C'est pas aussi puissant que les gestionnaires Linux, mais c'est le plus proche que macOS te laisse aller sans jailbreak.

Si tu passes la majorité de ton temps en terminal + éditeur + navigateur, ça vaut 30 minutes de setup. Ton workflow t'en sera reconnaissant.

---

*Tous les fichiers de config gérés avec chezmoi, synchronisés sur mon MacBook Pro, Mac Mini, desktop Fedora et Raspberry Pi.*
