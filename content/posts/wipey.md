---
title: "Wipey: I Built a macOS App Because I Kept Accidentally Sending Emails While Cleaning My Keyboard"
date: 2026-03-09T21:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "A macOS app that locks keyboard and trackpad during cleaning. Built in Swift, distributed via Homebrew."
categories: ["macOS", "Engineering"]
tags: ["swift", "macos", "app", "productivity", "open-source", "engineering"]
cover:
  image: /images/covers/wipey.webp
  alt: "Wipey macOS keyboard lock app"
---

Every developer has been there. You're at your desk, keyboard getting sticky from coffee or dust, so you grab a microfiber cloth and start cleaning. Three seconds later you've somehow triggered three keyboard shortcuts, opened Slack, sent an incomplete message to a colleague, and switched to a random Neovim buffer. All because your fingers brushed the keys while wiping.

The problem is stupid. The solution was obvious. So I built it.

## The Problem (That Nobody Talks About)

It sounds ridiculous, but it happens to everyone:

1. Start cleaning keyboard with cloth
2. Accidentally touch keys (muscle memory is weird when your hands are busy)
3. Send half-finished email: "Hey, just wanted to che—"
4. Hit Cmd+W, close the wrong window
5. Somehow activate Spotlight and search for "jdksl"

I looked for existing solutions. Nothing fit. Most screen-locking apps are full-featured security tools—overkill for "I don't want to accidentally hit Cmd+S while dusting." I needed something dumb-simple: lock input for 30 seconds while I clean.

## Wipey: Simple by Design

Wipey is a tiny macOS menu bar app. You set a global hotkey (I use Cmd+Shift+L), activate it, clean your keyboard for a minute, and input is completely locked. No trackpad clicks, no keyboard presses, no accidental disasters.

Written in Swift with native APIs, it's about 200 lines of code. No bloat, no permissions required beyond what's necessary, and it distributes via Homebrew (no App Store tax, no sandboxing nonsense).

The architecture is minimal:

```swift
// Simplified: Listen for global hotkey
import Cocoa

class InputLock {
    private var eventTap: CFMachPort?

    func lockInput(duration: TimeInterval = 30) {
        eventTap = CGEvent.tapCreate(
            tap: .cghidEventTap,
            place: .headInsertEventTap,
            options: .defaultTap,
            eventsOfInterest: CGEventMask((1 << CGEventType.keyDown.rawValue) |
                                          (1 << CGEventType.mouseMoved.rawValue)),
            callback: { _, _, event, _ in event } // Suppress all input
        )

        CFMachPortCreateRunLoopSource(kCFAllocatorDefault, eventTap!, 0)
        DispatchQueue.main.asyncAfter(deadline: .now() + duration) {
            self.unlockInput()
        }
    }

    func unlockInput() {
        CFMachPortInvalidate(eventTap)
        eventTap = nil
    }
}
```

The real work is done by `CGEventTap` — a macOS API that intercepts keyboard and mouse events. When Wipey is active, every input event gets suppressed. When the timer expires, the tap is removed and everything works normally again.

## Distribution Without the Gatekeepers

Wipey is [open-source on GitHub](https://github.com/jsoyer/Wipey) and available via Homebrew:

```bash
brew tap jsoyer/tools
brew install wipey
```

No App Store, no annual fee, no review process. Just a Homebrew tap that points to GitHub releases. Users can inspect the code, build it themselves if they want, or trust the binary. This is how software should work for utilities.

## Why This Matters (Even If It Seems Dumb)

Building Wipey taught me something that shapes how I think about tools now:

The best solutions are often the ones that solve *exactly one problem* for *exactly the right audience*. Not everyone needs a keyboard locker. But everyone who maintains a laptop and cleans it occasionally? They feel seen when you build the tool they didn't know they needed.

Wipey has accumulated a few hundred stars on GitHub. People use it. People file issues about adding duration options, or per-app locking (lock only when Notion is active, for example). Every feature request is reasonable because the scope stayed tight.

## The Meta-Lesson

I spent maybe 2 hours building Wipey. The problem it solves takes 5 seconds to explain. That ratio—"minimal code for maximum relief"—is what I chase now in everything I build.

Most software is overengineered. Wipey is the opposite: it's underengineered on purpose, and it's better for it.

If you've ever sent a typo-laden email because of keyboard dust, grab Wipey. You'll thank yourself.
