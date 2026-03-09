---
title: "Atuin Self-Hosted: Encrypted Shell History Sync Across All Your Machines"
date: 2025-11-19T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Run your own encrypted shell history server on Raspberry Pi for seamless command sync"
categories: ["Homelab", "Tooling"]
tags: ["atuin", "shell", "terminal", "homelab", "raspberry-pi", "automation", "productivity"]
cover:
  image: /images/covers/atuin-self-hosted.webp
  alt: "Atuin Self-Hosted Shell History"
---

I work across three machines daily: MacBook Pro, Fedora desktop, and a Raspberry Pi in my homelab. Each has its own shell history — isolated, scattered, lost. I'd write a command on my Mac that fixes an issue, then hours later on Linux, I'd waste 10 minutes reconstructing it from memory. Or worse: I'd reboot and lose three months of `curl` one-liners.

Then I discovered **Atuin**.

Atuin replaces your shell's history with a fast, searchable database that syncs across machines. Unlike `history | grep` or Ctrl+R, Atuin lets you query history by exit code, working directory, command type, and timestamp. And you can **self-host it** — I run my own Atuin server on my Raspberry Pi, encrypted end-to-end, no clouds involved.

### The Problem with Shell History

Your shell's default history is... terrible:
- **Lost on reboot**: If your shell crashes, unsaved history vanishes
- **Not searchable**: `history | grep docker` gets 500 matches. Good luck.
- **Not synced**: New machine? Lost all your command knowledge
- **No metadata**: When did I run that? From which directory? Did it fail?

I once spent 30 minutes rewriting a complex `find` command because I couldn't remember it. The original was in my history on my work Mac, but I was on my personal laptop. That was the moment I decided: there had to be a better way.

### What Atuin Does

Atuin replaces your shell's history with **structured data**:

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

Now you can search intelligently:
```bash
# Find all docker commands that succeeded
atuin search --exit 0 docker

# Find all commands in my project directory
atuin search --cwd /projects/myapp

# Find failed SSH attempts
atuin search --exit 1 ssh

# Find recent commands (last 7 days)
atuin search --days 7 curl

# Find commands by duration (slow queries)
atuin search --duration 5000 select
```

And here's the kicker: **all of this syncs across machines**, encrypted end-to-end. Your shell history becomes portable.

### Self-Hosting Atuin on Raspberry Pi

Running Atuin in the cloud (their hosted service) is fine, but I prefer owning my data. Here's how I set it up on my Raspberry Pi 4.

**Prerequisites:**
- Raspberry Pi 4 (or any Linux server)
- Docker + Docker Compose
- Basic networking (port forwarding or Tailscale)

**Docker Compose setup** (`~/atuin/docker-compose.yml`):
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
      # Database config
      ATUIN_DB_URI: "sqlite:///local/atuin.db"
      # Encryption key (generate with `head -c 32 /dev/urandom | base64`)
      ATUIN_DB_KEY: "YOUR_SECRET_KEY_HERE"
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

**Start the server:**
```bash
cd ~/atuin
docker-compose up -d
```

**Verify it's running:**
```bash
curl http://localhost:8888/health
# Response: { "status": "ok" }
```

### Exposing Atuin Safely

I run Atuin behind an **nginx reverse proxy** with SSL (using Let's Encrypt):

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

Or, **simpler approach**: Use Tailscale. My Atuin server is only accessible within my Tailscale network, so no port forwarding needed. Just point clients to `atuin.jerome.ts.net`.

### Configuring Atuin Clients

On each machine (MacBook, Fedora, Raspberry Pi), install Atuin:
```bash
brew install atuin        # macOS
# or
cargo install atuin       # Fedora/Linux
```

**Client config** (`~/.config/atuin/config.toml`):
```toml
# Account settings
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

# Shell integration
auto_sync = true
```

**Initiate sync on first run:**
```bash
atuin login
# Opens browser to register account on your Atuin server
# Returns credentials, stores them securely
```

**Optional: Chezmoi template** (for multiple machines with the same config):
```toml
# ~/.config/atuin/config.toml.tmpl
username = "jerome"
sync_address = "{{ if eq .chezmoi.os "darwin" }}https://atuin.jeromesoyer.com{{ else }}https://atuin.jerome.ts.net{{ end }}"
sync_frequency = 5m
```

### Shell Integration

Atuin replaces your `Ctrl+R` with **fuzzy search**:

```bash
# Press Ctrl+R on any machine
# Opens Atuin search interface
# Type "docker" → shows all docker commands ever
# Type "docker push" → filters to that
# Arrow up/down to navigate
# Enter to execute
```

Compatible with:
- Zsh (default in most configs)
- Bash
- Nushell
- Fish

**Zsh integration** (added to `~/.zshrc`):
```bash
eval "$(atuin init zsh)"

# Optional: Custom keybinding
bindkey '^R' __atuin_search_widget
```

### Real-World Example

Let me show you what changed my workflow:

**Before Atuin:**
I needed to remember a complex `find` command to locate all TypeScript files modified in the last 3 days, excluding node_modules:
```bash
find ~/projects -type f -name "*.ts" -mtime -3 ! -path "*/node_modules/*"
```

Used it on my MacBook. Rebooted. Gone forever. Had to reconstruct it on Fedora 20 minutes later.

**After Atuin:**
```bash
atuin search --cwd ~/projects --days 3 find ts
# Instant: all my `find` commands in that directory
# Select the right one
# Execute it again
```

Or better yet:
```bash
atuin search --exit 0 --days 3 find
# Just succeeded commands (exit code 0)
# Saves me from repeating failed attempts
```

### Performance

Atuin is **fast** even on Raspberry Pi:
- Indexing: 10,000 commands ≈ 50ms
- Search: Instant (local SQLite)
- Sync: Background, doesn't block shell

My Atuin database is ~5MB with 15,000+ commands across 8 months. Searches complete in <50ms.

### Encryption

Here's the security model:
- **At rest**: Database encrypted with your passphrase
- **In transit**: TLS (HTTPS)
- **End-to-end**: Your client encrypts before sending, server stores encrypted blobs

Your Atuin server **cannot read your commands**. Even if someone breaks into my Raspberry Pi, the history is encrypted.

### Lessons Learned

1. **Start with Docker Compose**: Easier than manual setup, handles dependencies.

2. **Back up your database**: SQLite file in `./data/atuin.db`. Sync to S3 or your NAS.

3. **Use Tailscale for privacy**: No need to expose Atuin to the internet. Add it to your VPN.

4. **Multiple machines need different sync_frequency**: Your Mac can sync every 5 minutes, but your Raspberry Pi might run every hour.

5. **History filter wisely**: I exclude `cargo`, `npm`, `make` — too noisy. But I keep `docker`, `git`, `ssh`.

### The Result

Now my shell history is:
- **Searchable** across 8 months and 15,000+ commands
- **Synced** across MacBook + Fedora + Raspberry Pi
- **Encrypted** from client to server
- **Self-hosted** on hardware I control
- **Fast** — queries complete in milliseconds

I never lose a command again. Complex one-liners, debugged queries, proven SSH invocations — they're all available instantly on any machine.

That's the power of treating your shell history as a **first-class database**.

---

*Atuin server running in Docker on Raspberry Pi 4, synced via Tailscale. Database backed up daily to my NAS.*
