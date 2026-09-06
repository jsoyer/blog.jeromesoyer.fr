---
title: "Omarchy on MacBook Pro: Zero-Friction Arch Linux on Apple T2 Hardware"
date: 2026-09-06T10:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "Installing Arch Linux on an Apple T2 MacBook used to be an ordeal. With Omarchy, everything works on first boot with essentially zero post-install setup."
categories: ["Linux", "Hardware", "Tooling"]
tags: ["omarchy", "arch", "macbook", "apple", "hyprland", "linux", "hardware", "dotfiles"]
cover:
  image: /images/covers/omarchy-macbook-pro.webp
  alt: "Omarchy on MacBook Pro"
---

### The Spark: Waking Up Apple Hardware

I have always had an appreciation for Apple hardware. The milled aluminum unibody chassis, the color-accurate Retina display, and the Force Touch trackpad—whose precision remains unmatched in the PC laptop world. Mechanically, these machines are industrial masterpieces.

In an earlier post on [resurrecting Intel Macs for a 128GB homelab](/posts/intel-mac-homelab/), I wrote about giving a 2013 Mac Pro and a 2018 Mac Mini a second life under Fedora and Windows. But on a daily laptop, recent macOS releases have become increasingly frustrating: background telemetry accumulates, the OS locks down further, and machines with massive raw processing power end up throttled by software choices that no longer align with a terminal-centric, agent-driven CLI workflow.

The spark came from an experience shared by Pierre Guillemot ([@pgllmt on X](https://x.com/pgllmt/status/2096538975443841345)). Seeing his feedback on running **Omarchy** on Mac hardware and rediscovering a blistering, razor-sharp Linux environment on Apple silicon predecessors pushed me to test it on my own **15-inch MacBook Pro**.

The promise sounded almost too good to be true: an opinionated, modern Arch Linux distribution powered by Hyprland, ready to use out of the box, with zero hardware hassle on Mac. I flashed a USB drive, ran the installer, and what followed exceeded every expectation.

---

### The Historical Trauma: Linux on T2 MacBooks

To understand why Omarchy feels like a small engineering miracle, you have to remember what running Linux on an Apple machine equipped with the **Apple T2 Security Chip** (2018–2020 models) used to require.

On these machines (such as my MacBookPro15,3 with its 8-core Intel Core i9-9980HK, AMD Radeon Pro Vega 20 GPU, and 32GB RAM), the T2 chip is not just a cryptographic co-processor:
- It acts as an internal PCIe bridge and bus controller. The internal keyboard and trackpad communicate via virtual USB routed through the T2.
- It controls internal NVMe SSD access with on-the-fly hardware encryption.
- It drives the audio pipelines (DSPs, microphones, speaker amplifiers) and the FaceTime HD camera.
- It governs fan curves and SMC thermal telemetry.

In a conventional Linux installation on a T2 Mac, the standard experience was notoriously difficult:
1. **Dead peripherals at boot:** Without a dedicated patched kernel (`linux-t2`), neither the keyboard nor the trackpad responded in the installer.
2. **The Broadcom Wi-Fi trap:** The Broadcom BCM4364 chipset attempted hardware offloading for the 4-way WPA handshake, which consistently failed on modern WPA2/WPA3 transition access points. NetworkManager would loop endlessly, falsely claiming your password was wrong.
3. **Mute speakers:** No sound output without custom firmware blobs and hand-tuned ALSA/PipeWire configuration profiles.
4. **Jet-engine fans:** Fans ran either at 100% full blast indefinitely or did not trigger at all, threatening thermal throttling on the Core i9.

Getting Arch Linux running cleanly meant cross-referencing wiki pages, compiling out-of-tree DKMS modules, wrestling with initramfs configurations, and dreading every kernel update.

---

### The Omarchy Approach: "Omakase" Hardware Detection

This is where **Omarchy** fundamentally shifts the equation. The distribution—created by David Heinemeier Hansson (DHH) and supported by the Omacom Foundation—takes the Japanese *omakase* philosophy ("I leave it up to you") to the operating system: strong, polished architectural defaults ready to roll.

Beyond the desktop stack (Hyprland Wayland compositor, reactive Quickshell status bar and launcher, pre-configured Neovim), Omarchy includes an automated hardware detection suite that handles machine-specific quirks during installation.

When the installer runs, it inspects PCI identifiers. As soon as it spots the signature of the Apple T2 chip (`106b:1801` or `106b:1802`), it provisions everything required:

```bash
# Extracted from Omarchy's hardware scripts (/usr/share/omarchy/install/hardware/apple/fix-t2.sh)
if lspci -nn | grep "106b:180[12]" >/dev/null; then
  echo "Detected MacBook with T2 chip. Installing support items..."

  omarchy-pkg-add \
    linux-t2 \
    linux-t2-headers \
    apple-t2-audio-config \
    apple-bcm-firmware \
    t2fanrd
...
```

In a single automated pass:
- **T2-specific kernel:** Installs `linux-t2` (version 7.1.8-arch1-Watanare-T2) and its companion headers.
- **Initramfs provisioning:** Injects necessary modules (`t2bce_vhci`, `usbhid`, `hid_apple`) into `mkinitcpio.conf.d/apple-t2.conf` so the keyboard and trackpad work immediately at disk decryption prompts.
- **Silent thermal control:** Activates `t2fanrd.service`, a daemon written in Rust that manages dual-fan curves dynamically based on T2 thermal sensors.
- **Broadcom Wi-Fi fix:** Configures `options brcmfmac feature_disable=0x82000` in `/etc/modprobe.d/brcmfmac.conf`, handing the WPA handshake back to software `wpa_supplicant`. Zero Wi-Fi authentication issues.
- **Bootloader flags:** Sets required Limine boot parameters (`intel_iommu=on iommu=pt pm_async=off mem_sleep_default=deep`) for clean deep sleep and wake cycles.

No forum digging, no manual compilation, no trial-and-error troubleshooting.

---

### First Boot: Zero Surprises, Complete Functionality

The moment of truth is the first reboot. No fallback USB drive needed, no black screen, no panic.

The machine boots through Limine, initializes the T2 kernel, and lands in the Omarchy environment within seconds. The hardware support inventory is immediately apparent:

| Hardware Component | Omarchy Status | Technical Notes |
| :--- | :--- | :--- |
| **Keyboard & Backlight** | 🟢 100% Functional | Backlight managed via `apple::kbd_backlight` |
| **Force Touch Trackpad** | 🟢 100% Functional | Haptic feedback click, smooth multitouch gestures |
| **Wi-Fi 802.11ac** | 🟢 100% Functional | Broadcom BCM4364 associates immediately |
| **Bluetooth** | 🟢 100% Functional | `hci_bcm4377` daemon active |
| **Audio & Speakers** | 🟢 100% Functional | PipeWire 1.6 + `apple-t2-audio-config`, rich stereo sound |
| **FaceTime HD Camera** | 🟢 100% Functional | Recognized natively through `uvcvideo` driver |
| **Dual GPU (Intel + AMD Vega 20)** | 🟢 100% Functional | Native Wayland rendering on `amdgpu` with Vulkan 1.4 |
| **Retina 2880x1800 Display** | 🟢 100% Functional | Sharp pixel density, crisp font rendering, zero tearing |
| **Fans & Thermals** | 🟢 100% Functional | Dynamically controlled via the `t2fanrd` Rust daemon |

Even the Touch Bar initializes with full backlight control (`appletb_backlight`) and functional function keys.

---

### What I Had to Configure Afterwards: Literally 5 Lines

On most laptop Linux setups, post-installation accounts for the majority of the time: tweaking fractional scaling, fixing keyboard layouts, diagnosing audio crackles, or debugging sleep drain.

Here, my personal configuration was restricted to **two files** in `~/.config/hypr/`.

First, setting the Mac AZERTY layout and natural scrolling in `~/.config/hypr/input.lua`:

```lua
hl.config({
  input = {
    -- French Macintosh AZERTY on the built-in ISO keyboard
    kb_layout = "fr",
    kb_variant = "mac",
    kb_model = "applealu_iso",
    kb_options = "compose:caps,shift:both_capslock_cancel",

    touchpad = {
      -- Mac-style natural scrolling
      natural_scroll = true,
      clickfinger_behavior = true,
    },
  },
})

-- Three-finger horizontal swipe to switch workspaces
hl.gesture({ fingers = 3, direction = "horizontal", action = "workspace" })
```

Second, adjusting the monitor scale for the 15" Retina panel in `~/.config/hypr/monitors.lua`:

```lua
local omarchy_monitor_scale = 1.25

hl.monitor({ output = "", mode = "preferred", position = "auto", scale = omarchy_monitor_scale })
```

That was it. No arcane shell commands, no udev tinkering, no experimental ALSA patches. Within three minutes, the laptop was fully tuned for daily production work.

---

### The Verdict: A High-Performance Dev Machine

On this 8-core, 16-thread Core i9 MacBook Pro with 32GB of RAM, Omarchy feels exceptionally fast.

At idle, Wayland consumes around 5GB of RAM with multiple terminal windows, CLI tools, btop, and background daemons active. The responsiveness of Hyprland combined with the Retina panel makes the machine feel revitalized:
- **Zero latency:** Workspace switching via keyboard shortcuts or 3-finger touchpad gestures is instantaneous.
- **Near-silent operation:** The `t2fanrd` daemon keeps fan speeds around 2,700 RPM during dev workflows, eliminating the persistent heat spikes that macOS background indexing often triggered.
- **Distraction-free environment:** Neovim, Kitty, Ghostty, and CLI agents run in an unencumbered environment aligned with the [Least Privilege](/posts/securing-ai-agents/) philosophy.

### Takeaway

If you have an Intel-era MacBook that has been sidelined or bogged down by recent macOS versions, the era where running Linux meant sleepless nights of debugging is over.

Omarchy demonstrates that a Linux distribution can offer uncompromising performance and control while delivering an installation experience as smooth as a mainstream commercial OS. Apple hardware gets to do what it does best: provide exceptional industrial design and build quality for a fast, open, and liberated Linux environment.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
