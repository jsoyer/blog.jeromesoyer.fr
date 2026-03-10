---
title: "Kitty Terminal: A Deep Dive Into the GPU-Accelerated Beast"
date: 2025-08-20T11:45:00+02:00
draft: false
author: "Jerome Soyer"
description: "Beyond just opening tabs — Kitty's kittens, layouts, scripting, and why it's been my primary terminal for years."
categories: ["Tooling", "Terminal"]
tags: ["kitty", "terminal", "productivity", "gpu", "cli", "automation"]
cover:
  image: /images/covers/kitty-deep-dive.webp
  alt: "Kitty Terminal Deep Dive"
---

Most developers pick a terminal emulator the way they pick a font: once, slightly randomly, and then never change. I was the same — until I tried **[Kitty](https://sw.kovidgoyal.net/kitty/)** and realized I'd been leaving performance and capability on the table for years.

This isn't a "why Kitty over iTerm2" post. This is what Kitty can actually *do* that you probably don't know about.

### Why Kitty?

The pitch is simple: GPU-accelerated rendering, scriptable via Python, and a concept called **kittens** (small terminal programs that extend functionality). It's fast, it's programmable, and it doesn't get in your way.

```ini
# kitty.conf — minimal starting point
font_family      JetBrainsMono Nerd Font
font_size        14.0
background_opacity 0.95
cursor_shape     beam
scrollback_lines 10000
```

### Layouts: The Hidden Superpower

Kitty has a tiling layout system built-in. No tmux required.

```ini
# Available layouts
enabled_layouts tall, fat, grid, horizontal, vertical, stack
```

Cycle through them with `ctrl+shift+l`. My most-used:

- **tall** — one main pane left, stack of smaller panes right
- **stack** — all windows stacked, switch with `ctrl+shift+[` / `]`

### Kittens: Extending Kitty With Python

Kittens are small programs that run inside Kitty and have access to its internals. The built-in ones are already useful:

```bash
# diff with syntax highlighting
kitty +kitten diff file1.py file2.py

# SSH with full terminal capabilities
kitty +kitten ssh user@host

# Unicode input
kitty +kitten unicode_input

# Clipboard management
kitty +kitten clipboard
```

You can write your own kittens in Python with full access to the terminal state, running processes, windows, and tabs.

### Remote Control: Script Everything

This is where Kitty gets serious. Enable it:

```ini
# kitty.conf
allow_remote_control yes
listen_on unix:/tmp/kitty
```

Now you can control Kitty from any script:

```bash
# Open a new tab named "logs"
kitty @ new-window --title logs --type tab

# Send a command to a specific window
kitty @ send-text --match title:logs "tail -f /var/log/app.log\n"

# Focus a window
kitty @ focus-window --match title:editor

# Get info on all windows
kitty @ ls
```

This is the foundation of my [Raycast Kitty extension](/posts/raycast-kitty/) — it's all just `kitty @` commands under the hood.

### YAML Launch Configs

My favorite feature: define entire workspace layouts in YAML and launch them with one command.

```yaml
# ~/.config/kitty/launch-configs/web-dev.yaml
layout: tall
tabs:
  - name: editor
    cwd: ~/projects/myapp
    command: nvim .
  - name: server
    cwd: ~/projects/myapp
    command: npm run dev
  - name: logs
    cwd: ~/projects/myapp
    command: tail -f logs/app.log
  - name: shell
    cwd: ~/projects/myapp
```

One command launches your entire dev environment, perfectly arranged.

### Performance

On a 4K display with a lot of text, the difference between a GPU-accelerated terminal and a non-accelerated one is measurable. Kitty renders text on the GPU — no jank when scrolling through large log files or `git log` on a big repository.

### My Full Config

Key settings I recommend beyond the defaults:

```ini
# Performance
repaint_delay 10
input_delay 3
sync_to_monitor yes

# Window management
window_padding_width 8
placement_strategy center
hide_window_decorations titlebar-only  # macOS

# Tab bar
tab_bar_edge top
tab_bar_style powerline
tab_powerline_style round

# Keyboard shortcuts (using vim-style navigation)
map ctrl+h neighboring_window left
map ctrl+l neighboring_window right
map ctrl+k neighboring_window up
map ctrl+j neighboring_window down
```

### The Raycast Connection

I built a Raycast extension specifically to drive Kitty: search tabs, create windows, launch YAML configs, all without touching the keyboard. It's [available on the Raycast store](https://www.raycast.com/jsoyer/kitty-window-manager). More on that in [its own post](/posts/raycast-kitty/).

### Next Steps

- **Set up your editor:** [My Neovim Setup in 2025](/posts/neovim-setup/) — configure Neovim to work seamlessly inside Kitty.
- **Automate with Raycast:** [Raycast Kitty Extension](/posts/raycast-kitty/) — search tabs, launch workspace configs, all from Raycast.

---

*Full config available in my [dotfiles](https://github.com/jsoyer)*
