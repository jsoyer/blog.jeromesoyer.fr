---
title: "Atuin en self-hosted : historique shell chiffré et synchronisé sur toutes vos machines"
date: 2025-11-19T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Lancez votre propre serveur d'historique shell chiffré sur Raspberry Pi pour une synchronisation transparente"
categories: ["Homelab", "Tooling"]
tags: ["atuin", "shell", "terminal", "homelab", "raspberry-pi", "automation", "productivite"]
cover:
  image: /images/covers/atuin-self-hosted.webp
  alt: "Atuin Self-Hosted Historique Shell"
---

Je travaille sur trois machines chaque jour : MacBook Pro, desktop Fedora et un Raspberry Pi dans mon homelab. Chacun a son propre historique shell — isolé, éparpillé, perdu. J'écrivais une commande sur mon Mac qui réglait un bug, puis des heures après sur Linux, je perdais 10 minutes à la reconstruire de mémoire. Ou pire : je redémarrais et perdais trois mois de `curl` one-liners.

Puis j'ai découvert **Atuin**.

Atuin remplace l'historique de ton shell par une base de données rapide et cherchable qui se synchronise entre machines. Contrairement à `history | grep` ou Ctrl+R, Atuin te permet de chercher l'historique par code de sortie, répertoire courant, type de commande, et timestamp. Et tu peux **l'auto-héberger** — je lance mon propre serveur Atuin sur mon Raspberry Pi, chiffré de bout en bout, sans clouds.

### Le problème : l'historique shell par défaut

L'historique par défaut de ton shell, c'est... catastrophique :
- **Perdu au redémarrage** : Si le shell plante, l'historique non sauvegardé disparaît
- **Pas cherchable** : `history | grep docker` retourne 500 matchs. À toi de fouiller.
- **Pas synchronisé** : Nouvelle machine ? Adieu ton savoir-faire des commandes
- **Pas de métadonnées** : Quand j'ai lancé ça ? D'où ? Est-ce que ça a marché ?

Je me suis un jour passé 30 minutes à réécrire une commande `find` complexe parce que je ne la retenais pas. L'originale était dans mon historique sur mon MacBook pro, mais j'étais sur mon laptop perso. C'est là que j'ai décidé : il devait y avoir une meilleure manière.

### Ce qu'Atuin fait

Atuin remplace l'historique de ton shell par des **données structurées** :

```json
{
  "id": "12e3f4c9",
  "command": "docker ps -a --filter status=exited",
  "cwd": "/home/jerome/projects/myapp",
  "exit_code": 0,
  "duration": 2340,
  "timestamp": 1709960430,
  "hostname": "macbook-pro",
  "shell": "zsh",
  "session": "s_1709960000"
}
```

Maintenant tu peux chercher intelligemment :
```bash
# Trouver toutes les commandes docker qui ont réussi
atuin search --exit 0 docker

# Trouver toutes les commandes dans mon répertoire de projet
atuin search --cwd /projects/myapp

# Trouver les tentatives SSH échouées
atuin search --exit 1 ssh

# Trouver les commandes récentes (7 derniers jours)
atuin search --days 7 curl

# Trouver les commandes lentes
atuin search --duration 5000 select
```

Et voilà le coup de grâce : **tout ça se synchronise entre machines**, chiffré de bout en bout. Ton historique shell devient portable.

### Auto-héberger Atuin sur Raspberry Pi

Lancer Atuin dans le cloud (leur service hébergé) c'est bien, mais je préfère posséder mes données. Voici comment j'ai configuré sur mon Raspberry Pi 4.

**Prérequis :**
- Raspberry Pi 4 (ou n'importe quel serveur Linux)
- Docker + Docker Compose
- Networking basique (port forwarding ou Tailscale)

**Configuration Docker Compose** (`~/atuin/docker-compose.yml`) :
```yaml
version: '3.8'

services:
  atuin-server:
    image: ghcr.io/atuinsh/atuin:latest
    container_name: atuin-server
    restart: unless-stopped
    environment:
      ATUIN_PORT: 8888
      ATUIN_HOST: 0.0.0.0
      ATUIN_LOG_LEVEL: info
      # Config base de données
      ATUIN_DB_URI: "sqlite:///local/atuin.db"
      # Clé de chiffrement (générer avec `head -c 32 /dev/urandom | base64`)
      ATUIN_DB_KEY: "VOTRE_CLE_SECRETE_ICI"
    volumes:
      - ./data:/local
    ports:
      - "8888:8888"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8888/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Lancer le serveur :**
```bash
cd ~/atuin
docker-compose up -d
```

**Vérifier qu'il tourne :**
```bash
curl http://localhost:8888/health
# Réponse : { "status": "ok" }
```

### Exposer Atuin de manière sûre

Je lance Atuin derrière un **reverse proxy nginx** avec SSL (Let's Encrypt) :

```nginx
# /etc/nginx/sites-available/atuin.example.com
server {
    listen 443 ssl http2;
    server_name atuin.example.com;

    ssl_certificate /etc/letsencrypt/live/atuin.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/atuin.example.com/privkey.pem;

    location / {
        proxy_pass http://localhost:8888;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

server {
    listen 80;
    server_name atuin.example.com;
    return 301 https://$server_name$request_uri;
}
```

Ou, **approche plus simple** : Utiliser Tailscale. Mon serveur Atuin est uniquement accessible au sein de mon réseau Tailscale, donc pas de port forwarding. Juste diriger les clients vers `atuin.jerome.ts.net`.

### Configurer les clients Atuin

Sur chaque machine (MacBook, Fedora, Raspberry Pi), installer Atuin :
```bash
brew install atuin        # macOS
# ou
cargo install atuin       # Fedora/Linux
```

**Config client** (`~/.config/atuin/config.toml`) :
```toml
# Paramètres de compte
username = "jerome"
sync_address = "https://atuin.example.com"
sync_frequency = 5m

# Keybindings
key_up = "up"
key_down = "down"

# UI
history_filter = ["cargo", "npm", "pnpm", "make"]
max_preview_height = 4
previewers_height = 2

# Intégration shell
auto_sync = true
```

**Initialiser la synchro au premier lancement :**
```bash
atuin login
# Ouvre le navigateur pour s'enregistrer sur ton serveur Atuin
# Retourne les credentials, les sauvegarde de manière sécurisée
```

**Optionnel : Template Chezmoi** (pour plusieurs machines avec la même config) :
```toml
# ~/.config/atuin/config.toml.tmpl
username = "jerome"
sync_address = "{{ if eq .chezmoi.os "darwin" }}https://atuin.jeromesoyer.com{{ else }}https://atuin.jerome.ts.net{{ end }}"
sync_frequency = 5m
```

### Intégration shell

Atuin remplace ton `Ctrl+R` par une **recherche fuzzy** :

```bash
# Appuyer Ctrl+R sur n'importe quelle machine
# Ouvre l'interface de recherche Atuin
# Taper "docker" → affiche toutes les commandes docker jamais lancées
# Taper "docker push" → filtre sur ça
# Flèches haut/bas pour naviguer
# Entrée pour exécuter
```

Compatible avec :
- Zsh (par défaut dans la plupart des configs)
- Bash
- Nushell
- Fish

**Intégration Zsh** (ajouté à `~/.zshrc`) :
```bash
eval "$(atuin init zsh)"

# Optionnel : Keybinding personnalisé
bindkey '^R' __atuin_search_widget
```

### Exemple du monde réel

Voilà ce qui a changé mon workflow :

**Avant Atuin :**
Je devais mémoriser une commande `find` complexe pour localiser tous les fichiers TypeScript modifiés dans les 3 derniers jours, en excluant node_modules :
```bash
find ~/projects -type f -name "*.ts" -mtime -3 ! -path "*/node_modules/*"
```

Utilisée sur mon MacBook. Redémarrage. Disparue à jamais. Fallait la reconstruire sur Fedora 20 minutes après.

**Après Atuin :**
```bash
atuin search --cwd ~/projects --days 3 find ts
# Instantané : toutes mes commandes `find` dans ce répertoire
# Sélectionner la bonne
# L'exécuter à nouveau
```

Ou mieux :
```bash
atuin search --exit 0 --days 3 find
# Juste les commandes qui ont réussi (code 0)
# Me sauve de réexécuter des tentatives échouées
```

### Performance

Atuin est **rapide** même sur Raspberry Pi :
- Indexation : 10 000 commandes ≈ 50ms
- Recherche : Instantané (SQLite local)
- Sync : Arrière-plan, n'interfère pas avec le shell

Ma base de données Atuin fait ~5MB avec 15 000+ commandes sur 8 mois. Les recherches complètent en <50ms.

### Chiffrement

Voici le modèle de sécurité :
- **Au repos** : Base de données chiffrée avec ta passphrase
- **En transit** : TLS (HTTPS)
- **De bout en bout** : Ton client chiffre avant d'envoyer, le serveur stocke des blobs chiffrés

Ton serveur Atuin **ne peut pas lire tes commandes**. Même si quelqu'un hack mon Raspberry Pi, l'historique est chiffré.

### Leçons apprises

1. **Commencer avec Docker Compose** : Plus facile que setup manuel, gère les dépendances.

2. **Backup ta base de données** : Fichier SQLite en `./data/atuin.db`. Sync vers S3 ou ton NAS.

3. **Utiliser Tailscale pour la privacy** : Pas besoin d'exposer Atuin à Internet. L'ajouter à ton VPN.

4. **Plusieurs machines besoin de sync_frequency différentes** : Ton Mac peut syncer chaque 5 minutes, mais ton Raspberry Pi peut tourner chaque heure.

5. **Filtrer l'historique intelligemment** : J'exclue `cargo`, `npm`, `make` — trop bruyant. Mais je garde `docker`, `git`, `ssh`.

### Le résultat

Maintenant mon historique shell est :
- **Cherchable** sur 8 mois et 15 000+ commandes
- **Synchronisé** sur MacBook + Fedora + Raspberry Pi
- **Chiffré** de client à serveur
- **Auto-hébergé** sur du hardware que je contrôle
- **Rapide** — les queries complètent en millisecondes

Je ne perds jamais une commande. Les one-liners complexes, les queries debuggées, les invocations SSH éprouvées — tout est disponible instantanément sur n'importe quelle machine.

C'est la puissance de traiter ton historique shell comme une **base de données de première classe**.

---

*Serveur Atuin tournant en Docker sur Raspberry Pi 4, synchronisé via Tailscale. Base de données sauvegardée quotidiennement sur mon NAS.*
