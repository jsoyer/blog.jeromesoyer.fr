---
title: "Aerospace + Sketchybar: My Keyboard-Driven macOS Setup"
date: 2026-03-09T18:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "Tiling window manager + scriptable menubar for keyboard-driven macOS productivity"
categories: ["macOS", "Tooling"]
tags: ["macos", "aerospace", "sketchybar", "automation", "productivity", "cli", "dotfiles"]
cover:
  image: /images/covers/aerospace-sketchybar.webp
  alt: "Aerospace Sketchybar macOS Setup"
---

I've been using macOS for years, but one thing always bothered me: the lack of a keyboard-driven window manager. Stage Manager feels like a Fisher-Price toy, Mission Control is chaotic, and alt-tabbing between windows is inefficient. I spent too much time reaching for the mouse.

Then I discovered **Aerospace** — a tiling window manager for macOS that doesn't require disabling System Integrity Protection. Combined with **Sketchybar** (a scriptable replacement for macOS's menu bar), I've built a setup that feels less like macOS and more like i3 or Hyprland on Linux. Except it works seamlessly on my MacBook Pro.

### The Problem with macOS Window Management

Apple's built-in window management sucks if you're a keyboard person:
- **Mission Control**: Swipe up, move your eye to tiny preview, click. That's 3 seconds per task switch.
- **Stage Manager**: Feels like a sidebar that tries too hard.
- **Window snapping**: Half-screen snapping exists, but it's limited and clunky.

I was working with 4-5 windows open constantly — Neovim, browser, Slack, debug logs, tests. Without tiling, I either had overlapping windows (tedious switching) or constantly resizing. I wanted **workspaces** and **tiling** like Linux users get by default.

### Enter Aerospace

**Aerospace** is a lightweight tiling window manager written in Swift. No SIP disabled. No system hacks. Just a config file and keyboard shortcuts.

**Installation:**
```bash
brew install nikitabobko/tap/aerospace
```

**Basic config** (`~/.aerospace.toml`):
```toml
# Start each workspace on its own separate workspace
start-at-login = true

[mode.main.binding]
# Focus windows (vim-style hjkl)
alt-h = 'focus left'
alt-l = 'focus right'
alt-j = 'focus down'
alt-k = 'focus up'

# Move windows
alt-shift-h = 'move left'
alt-shift-l = 'move right'
alt-shift-j = 'move down'
alt-shift-k = 'move up'

# Workspace switching (Alt + number)
alt-1 = 'workspace 1'
alt-2 = 'workspace 2'
alt-3 = 'workspace 3'
alt-4 = 'workspace 4'
alt-5 = 'workspace 5'

# Move window to workspace
alt-shift-1 = 'move-node-to-workspace 1'
alt-shift-2 = 'move-node-to-workspace 2'

# Split and fullscreen
alt-e = 'layout tiles horizontal'
alt-o = 'layout tiles vertical'
alt-shift-e = 'layout accordion horizontal'
alt-shift-o = 'layout accordion vertical'
alt-shift-f = 'fullscreen'

# Close window
alt-w = 'close'
```

What I love:
- **Workspace isolation**: Alt+3 takes me to workspace 3 with my debug tools. Alt+1 is email/chat. No mixing.
- **Modal keys**: No collision with app shortcuts. `Alt-H` focuses left in my Aerospace layer, but Vim still gets `H` for history.
- **Layouts**: Tiled (equal splits), accordion (stacked). Switch with one keystroke.
- **No bloat**: It's just window management, not a full DE like Yabai.

### Sketchybar: The Perfect Companion

Aerospace works great, but I wanted **visual feedback** of which workspace I'm in. That's where **Sketchybar** comes in.

Sketchybar is a replacement for macOS's menu bar. It's fully scriptable in Bash and Lua. I use it to:
1. **Show active Aerospace workspace** (highlighted in my status bar)
2. **Display CPU/memory** (live system stats)
3. **Battery percentage** (for my MacBook)
4. **Current time and date**
5. **Keyboard layout indicator** (because I switch between EN/FR/BÉPO)

**Installation:**
```bash
brew install sketchybar
brew services start sketchybar
```

**Basic Sketchybar config** (`~/.config/sketchybar/sketchybarrc`):
```bash
#!/bin/bash

# Set color scheme
export COLOR_BACKGROUND=0x1a1a1a
export COLOR_TEXT=0xffffff
export COLOR_ACCENT=0x61afef

# Workspace indicator - shows Aerospace workspaces
for i in {1..9}; do
  sketchybar --add item workspace.$i left \
    --set workspace.$i \
    label=$i \
    width=35 \
    align=center \
    click-script="aerospace workspace $i"
done

# System stats
sketchybar --add item cpu right \
  --set cpu update_freq=2 \
  --script '$PLUGIN_DIR/cpu.sh'

sketchybar --add item memory right \
  --set memory update_freq=2 \
  --script '$PLUGIN_DIR/memory.sh'

# Clock
sketchybar --add item clock right \
  --set clock update_freq=10 \
  --script 'date "+%H:%M:%S"'
```

**Plugin to sync Aerospace workspaces** (`$PLUGIN_DIR/aerospace_workspace.sh`):
```bash
#!/bin/bash
# Gets current Aerospace workspace from aerospace CLI
CURRENT=$(aerospace list-workspaces --focused)

for i in {1..9}; do
  if [ "$i" -eq "$CURRENT" ]; then
    sketchybar --set workspace.$i background.color=0x61afef
  else
    sketchybar --set workspace.$i background.color=0x1a1a1a
  fi
done
```

The magic: I click a workspace number in Sketchybar, it runs `aerospace workspace 5`. Or I press Alt+5. Both work.

### Chezmoi: Version Control for Both

Since my setup spans macOS + Fedora + Raspberry Pi, I manage both Aerospace and Sketchybar configs in **chezmoi**:

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

The `.tmpl` files let me customize workspaces and bindings per machine:

```toml
# .aerospace.toml.tmpl
start-at-login = {{ if eq .chezmoi.os "darwin" }}true{{ else }}false{{ end }}

[mode.main.binding]
alt-h = 'focus left'
# Workspace switching - adjust count based on machine
{{- if eq .chezmoi.hostname "macbook-pro" }}
# More workspaces for main machine
alt-9 = 'workspace 9'
{{- end }}
```

One `chezmoi apply` and both tools are configured consistently.

### Aerospace vs Yabai

People ask: why not **Yabai**? Yabai is more powerful — true scripting, more control. But Yabai requires **SIP disabled**, which I'm not comfortable doing on my work MacBook (security reasons). Aerospace just works without hacking macOS internals. Trade-off: less customization, but peace of mind.

### The Daily Feel

When I wake up my MacBook:

```
Alt+1  → Slack + Mail (workspace 1)
Alt+2  → Browser + Research (workspace 2)
Alt+3  → Neovim + Tests + Logs (workspace 3, usually split vertical)
Alt+4  → Zoom calls (fullscreen)
```

Window switching is now:
```
Alt+H  → Focus left window
Alt+J  → Focus window below
Alt+Shift+L  → Move window right
```

No mouse. No Mission Control. Just keyboard.

Sketchybar shows me the workspace indicators at a glance, system stats don't clutter the terminal, and everything feels snappy.

### Lessons Learned

1. **Start with safe defaults**: Aerospace's defaults are solid. Tweak bindings to match your muscle memory (I use vim hjkl).

2. **Sketchybar plugins are bash**: If you can write bash, you can extend your menu bar. No learning Swift.

3. **Test the config before restarting**: `aerospace reload` and `sketchybar --reload` catch syntax errors.

4. **Chezmoi templates save sanity**: If you manage multiple machines, use templates for workspace counts, workspace names, etc.

5. **Some apps don't play nicely**: Zoom, Figma, some IDEs have weird tiling behavior. You can float-except them:
   ```toml
   [[on-window-detected]]
   if.app-id = 'us.zoom.xos'
   then = ['layout floating']
   ```

### The Bottom Line

Aerospace + Sketchybar transformed my macOS experience. I'm faster, I reach for the mouse less, and my setup feels **intentional** rather than reactive. It's not as powerful as Linux window managers, but it's the closest macOS lets you get without jailbreaking your system.

If you spend most of your day in terminal + editor + browser, it's worth the 30 minutes to set up. Your workflow will thank you.

---

*All config files managed with chezmoi, synced across my MacBook Pro, Mac Mini, Fedora desktop, and Raspberry Pi.*
