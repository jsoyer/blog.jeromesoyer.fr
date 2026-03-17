---
title: "Yapee: I Rebuilt a PyLoad Manager Because Manifest V2 Broke It"
date: 2026-03-17T10:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "A modern browser extension for managing PyLoad downloads with encryption, real-time updates, and desktop integration."
categories: ["Tooling"]
tags: ["browser-extension", "pyload", "downloads", "privacy", "self-hosted"]
cover:
  image: /images/covers/yapee.webp
  alt: "Yapee browser extension"
---

If you self-host downloads with PyLoad, you've probably used **Yape** — the classic browser extension that lets you manage downloads without opening a web interface. It was simple, it worked, and then Google killed it. Manifest V2 was deprecated, and Yape was abandoned.

So I rebuilt it from scratch. **Yapee** is the spiritual successor: a modern browser extension for Chrome, Firefox, and Edge that handles everything the old extension did, plus features that make managing multiple PyLoad servers actually pleasant.

## Why PyLoad Still Matters

Before diving into Yapee, let's talk about why PyLoad is still relevant in 2026. If you download media files, eBooks, or archives, you know the pain: juggling multiple file hosters, managing quotas, dealing with captchas. PyLoad is a self-hosted download manager that:

- Manages multiple hosters (Rapidgator, Uploaded, Mediafire, 60+ sites)
- Handles authentication and quotas automatically
- Solves captchas with OCR
- Runs on your own infrastructure (no cloud, no tracking)

It works, but the web interface is clunky. You want to queue downloads without logging in every time. That's where Yape came in — and now Yapee takes its place.

## The Problem: Manifest V2 Is Dead

The original Yape worked fine until Google started sunsetting Manifest V2 in 2024. MV2 allowed persistent background scripts that could maintain connections to your PyLoad server indefinitely. Manifest V3 killed that model. Background scripts have limited lifetime, fetch APIs work differently, and persistent storage changed.

Rewriting for MV3 wasn't a small task — it meant rethinking how the extension maintains state, updates the UI, and communicates with PyLoad. The old Yape was abandoned. So I started from scratch.

## What Yapee Does

Yapee is a browser extension that lives in your toolbar (Chrome Side Panel on Chrome, Sidebar on Firefox). It shows:

- **Active downloads** with progress bars, speed, and ETA
- **Queue status** — paused, running, completed
- **Multiple servers** — switch between your PyLoad instances with one click
- **Dark mode** with system theme detection (respects your OS preference)

More importantly, it doesn't require you to remember your PyLoad password. Credentials are encrypted with **AES-GCM 256-bit** and stored locally. No server, no cloud sync, no risk of credentials leaking.

### Key Features

**Real-time monitoring:** The extension uses event-driven architecture to stay in sync with your PyLoad server. When a download completes, you get a notification — the UI doesn't poll constantly.

**Context menu integration:** Right-click any link in your browser, select "Add to PyLoad," and it queues. No copy-pasting links to the web interface.

**Multi-URL paste:** Paste 50 links at once. The extension parses them, filters duplicates, and queues them. Useful for batch downloads.

**Captcha solving in the popup:** Some hosters throw captchas. Yapee includes a popup that lets you solve them without leaving your current tab.

**Container file support:** Upload DLC, CCF, or RSDF container files directly from the extension.

**Keyboard shortcuts:** Don't reach for the mouse. Toggle the sidebar, pause/resume downloads, switch servers — all with custom keybinds.

**Download history:** See what you've downloaded and when. Useful for finding files you queued days ago.

**i18n:** English and French with manual override (switch languages without restarting).

**Desktop notifications:** Get notified when downloads complete, even if the extension isn't open.

## The Tampermonkey Companion Script

Here's where Yapee gets interesting for power users.

Most download sites have JavaScript overlays that hijack right-clicks or make it hard to grab the actual download link. I wrote a **Tampermonkey script** that works alongside Yapee on 60+ hosters (RapidGator, Uploaded, Mediafire, 1Fichier, Uptobox, etc.).

The script adds a **"Download with PyLoad"** button directly on the page. One click and your download is queued without copy-pasting. For hosters with captchas, it fills the captcha data and passes it to Yapee's popup automatically.

This is the workflow that makes Yapee worth using:

1. Browse a file hosting site
2. Click "Download with PyLoad"
3. Solve captcha if needed (Yapee handles it)
4. Your PyLoad server starts downloading

No web interface, no manual link extraction, no clipboard nonsense.

## Encryption and Privacy

Here's something I think about constantly: every browser extension with access to your PyLoad credentials is a potential leak vector. Most download managers require you to save credentials in plaintext or sync them to a cloud service.

Yapee does neither.

Credentials are encrypted with AES-GCM using a key derived from your PyLoad password. Even if someone extracts the extension's storage, they get ciphertext. The encryption happens locally, and the key is never transmitted.

When you add a PyLoad server:

1. You enter the URL and password
2. Yapee generates an AES key from the password
3. Credentials are encrypted and stored locally
4. The password is discarded from memory
5. Future requests decrypt credentials on-the-fly

No cloud, no third-party authentication, no token leaks.

## Multi-Server Support

If you run multiple PyLoad instances (one for slow downloads, one for quick grabs, one for torrents), you can add all of them to Yapee. A dropdown in the extension lets you switch servers instantly. Each server has its own encrypted credentials.

## Current State

Yapee is on version **3.8.1**. It's actively maintained and stable. I use it daily across Chrome and Firefox.

**What's included:**
- Chrome Side Panel (modern, native integration)
- Firefox Sidebar (Sidebar API)
- Edge support (Chromium-based)
- Tampermonkey companion script
- Desktop notifications
- Keyboard shortcuts
- Full i18n (EN/FR)

**Installation:**

Chrome/Edge: [chrome.google.com/webstore](https://chrome.google.com/webstore) — search for Yapee

Firefox: [addons.mozilla.org](https://addons.mozilla.org) — search for Yapee

Tampermonkey script: [github.com/jsoyer/yapee](https://github.com/jsoyer/yapee)

## Why This Matters

Rebuilding Yapee taught me something important about extensions: they're increasingly the glue between the web and your personal infrastructure. Most extensions are either abandoned or turning into tracking vectors.

Yapee respects your privacy because it's self-hosted. Your PyLoad server runs on your hardware. Your credentials never leave your machine. The extension is just a UI layer that talks directly to *your* infrastructure.

If you still use PyLoad, give Yapee a shot. It removes the friction from managing downloads across multiple hosters and servers.

## Credits

Yapee stands on the shoulders of **Yape** by Rémi Rigal. I'm grateful for the original tool that proved the concept. When Google killed Manifest V2, someone needed to rebuild it for the modern web. That someone turned out to be me.

---

**Source code:** [github.com/jsoyer/yapee](https://github.com/jsoyer/yapee)

**Report issues:** [github.com/jsoyer/yapee/issues](https://github.com/jsoyer/yapee/issues)
