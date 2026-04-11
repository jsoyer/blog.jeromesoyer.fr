#!/usr/bin/env python3
"""
Cover image generator for blog.jeromesoyer.fr
Produces 1200x630 PNG files using Catppuccin Mocha + per-article accent colors.

Usage:
    python3 scripts/generate_covers.py              # regenerate all
    python3 scripts/generate_covers.py rtk          # single slug
    python3 scripts/generate_covers.py --preview    # write to /tmp instead
    python3 scripts/generate_covers.py --webp       # also emit .webp alongside .png

Dependencies: Pillow  (pip install Pillow)
Fonts required (already in ~/.local/share/fonts/):
    JetBrainsMonoNerdFont-Bold.ttf
    JetBrainsMonoNerdFont-Medium.ttf
    JetBrainsMonoNerdFont-Regular.ttf
"""

from __future__ import annotations
import math
import sys
import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Canvas ────────────────────────────────────────────────────────────────────
W, H = 1200, 630

# ── Catppuccin Mocha base palette ─────────────────────────────────────────────
BASE   = (30,  30,  46)   # #1e1e2e  — main background
MANTLE = (24,  24,  37)   # #181825  — darker bg (left edge)
SURF0  = (49,  50,  68)   # #313244  — surface
SURF1  = (69,  71,  90)   # #45475a  — muted surface (domain text, dots)
TEXT   = (205, 214, 244)  # #cdd6f4  — primary text
SUB0   = (166, 173, 200)  # #a6adc8  — subtitle text

# ── Font paths ─────────────────────────────────────────────────────────────────
# Prefer fonts bundled alongside this script (works in CI).
# Fall back to user's local font directory for local runs.
_SCRIPT_FONTS = Path(__file__).parent / "fonts"
_LOCAL_FONTS  = Path.home() / ".local/share/fonts"
_FONT_DIR     = _SCRIPT_FONTS if (_SCRIPT_FONTS / "JetBrainsMonoNerdFont-Bold.ttf").exists() else _LOCAL_FONTS
FONT_BOLD   = str(_FONT_DIR / "JetBrainsMonoNerdFont-Bold.ttf")
FONT_MEDIUM = str(_FONT_DIR / "JetBrainsMonoNerdFont-Medium.ttf")
FONT_REG    = str(_FONT_DIR / "JetBrainsMonoNerdFont-Regular.ttf")

# ── Output directory ───────────────────────────────────────────────────────────
REPO_ROOT  = Path(__file__).parent.parent
OUT_DIR    = REPO_ROOT / "static/images/covers"


# ── Per-article definitions ────────────────────────────────────────────────────
# Each entry: slug, punchy_title, subtitle, tags, accent_hex, glyph
#
# Glyphs: short ASCII/unicode sequences that read as symbols in JetBrains Mono.
# Keep them 1-4 characters: they will be rendered at ~300px as ghost art.
# Good choices: $_, >_, {}, [], ~/, :(), fn, //,  *, &&, |>, 0x, %%

ARTICLES: list[tuple[str, str, str, list[str], str, str]] = [
    (
        "rtk",
        "RTK: Stop Burning Tokens",
        "60-90% token savings. One binary.",
        ["Rust", "AI", "Tools"],
        "#f38ba8",   # Red
        ">>",
    ),
    (
        "neovim-setup",
        "My Neovim Setup in 2026",
        "LSP, lazy.nvim, Telescope. A workflow that ships.",
        ["Editor", "Neovim"],
        "#94e2d5",   # Teal
        "{}",
    ),
    (
        "hivepilot",
        "HivePilot: Multi-Agent AI From Scratch",
        "Orchestration that actually ships.",
        ["Engineering", "AI"],
        "#cba6f7",   # Mauve
        ">_",
    ),
    (
        "dotfiles",
        "Dotfiles Revolution with chezmoi",
        "One tool to manage your entire dev environment.",
        ["DevOps", "macOS", "Linux"],
        "#89b4fa",   # Blue
        "~/",
    ),
    (
        "aerospace-sketchybar",
        "Aerospace + Sketchybar",
        "Keyboard-driven macOS. No mouse required.",
        ["macOS", "Tooling"],
        "#89dceb",   # Sky
        "[]",
    ),
    (
        "atuin-self-hosted",
        "Atuin Self-Hosted: Encrypted Shell History",
        "Sync your shell history across every machine.",
        ["Homelab", "Tooling"],
        "#a6e3a1",   # Green
        "^R",
    ),
    (
        "chezmoi-vs-alternatives",
        "chezmoi vs yadm vs stow",
        "Which dotfiles manager should you actually use?",
        ["DevOps", "Tooling"],
        "#74c7ec",   # Sapphire
        "~=",
    ),
    (
        "cv-pipeline",
        "I Built an AI Job Application Pipeline",
        "And applied to Anthropic with it.",
        ["Engineering", "AI"],
        "#fab387",   # Peach
        "fn",
    ),
    (
        "framework-fedora-atomic",
        "Framework + Fedora Atomic",
        "The case for an immutable operating system.",
        ["Linux", "Tooling"],
        "#f9e2af",   # Yellow
        "//",
    ),
    (
        "kitty-deep-dive",
        "Kitty Terminal: Deep Dive",
        "GPU-accelerated. Fast by design.",
        ["Tooling", "Terminal"],
        "#f5c2e7",   # Pink
        ":D",
    ),
    (
        "mise",
        "mise: One Tool for All Version Managers",
        "Replace nvm, rbenv, pyenv — all of them.",
        ["Tooling", "DevOps"],
        "#b4befe",   # Lavender
        "&&",
    ),
    (
        "modern-cli-tools",
        "Modern CLI Tools to Replace Your Defaults",
        "The 2026 terminal toolkit.",
        ["Tooling", "CLI"],
        "#89b4fa",   # Blue
        "|>",
    ),
    (
        "nushell",
        "Nushell: Why I Left Zsh Behind",
        "Structured data. Modern shell. Real power.",
        ["Tooling", "Terminal"],
        "#a6e3a1",   # Green
        "nu",
    ),
    (
        "paperless-homelab",
        "Going Paperless with Paperless-ngx",
        "OCR, auto-tagging, zero paper clutter.",
        ["Homelab", "Automation"],
        "#94e2d5",   # Teal
        "%%",
    ),
    (
        "raycast-kitty",
        "Controlling Kitty Terminal with Raycast",
        "Unleash the cat. Automate everything.",
        ["Tooling"],
        "#f5c2e7",   # Pink
        ">>",
    ),
    (
        "running-data-nerd",
        "How a Data Nerd Approaches Running",
        "Spoiler: too many spreadsheets.",
        ["Life", "Running"],
        "#fab387",   # Peach
        "[]",
    ),
    (
        "wipey",
        "Wipey: A macOS App I Had to Build",
        "Stop sending emails while cleaning your keyboard.",
        ["macOS", "Engineering"],
        "#eba0ac",   # Maroon
        "[]",
    ),
    # French-only posts that share cover slugs
    (
        "cave-numerique",
        "Ma Cave Numerique",
        "L'infrastructure maison, sans compromis.",
        ["Homelab", "Linux"],
        "#cba6f7",   # Mauve
        ":/",
    ),
    (
        "crypto-2026",
        "Crypto 2026: Ce Que J'ai Appris",
        "Rationalite, bruit, et signal dans le marche.",
        ["Finance", "Life"],
        "#f9e2af",   # Yellow
        "0x",
    ),
    (
        "yapee",
        "Yapee: PyLoad Browser Extension",
        "Manifest V3. Privacy-first. Multi-server.",
        ["Tooling", "Self-Hosted"],
        "#89dceb",   # Sky
        "dl",
    ),
    (
        "intel-mac-homelab",
        "Intel Mac Renaissance",
        "128GB Combined RAM Homelab.",
        ["Hardware", "macOS", "Linux"],
        "#89b4fa",   # Blue
        "i",
    ),
    (
        "synapse-ai-forge",
        "Synapse: Modular AI Forge",
        "RTX 5070 & Modular Deployment.",
        ["AI", "Fedora", "NVIDIA"],
        "#fab387",   # Peach
        "AI",
    ),
    (
        "ai-first-engineering",
        "AI-First Engineering",
        "650+ Skills Dotfiles Evolution.",
        ["AI", "DevOps", "Automation"],
        "#cba6f7",   # Mauve
        "$_",
    ),
]


# ── Background rendering ───────────────────────────────────────────────────────

def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

def _lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    t = max(0.0, min(1.0, t))
    return tuple(int(_lerp(c1[i], c2[i], t)) for i in range(3))

def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _make_background(accent: tuple[int, int, int]) -> Image.Image:
    """
    Three-zone composited background — all computed per-pixel, no numpy.

    Zone 1: Horizontal gradient  MANTLE (left) -> BASE (right), soft.
    Zone 2: Radial accent glow   anchored bottom-right corner.
    Zone 3: Top-left vignette    lifts brightness toward SURF0 subtly.
    """
    img = Image.new("RGB", (W, H))
    px  = img.load()

    for y in range(H):
        for x in range(W):
            # Zone 1 — horizontal gradient, left darker
            tx = x / (W - 1)
            bg = _lerp_color(MANTLE, BASE, tx * 0.65 + 0.18)

            # Zone 2 — radial accent glow, bottom-right anchor
            gx, gy = W * 0.92, H * 0.88
            dist = math.sqrt((x - gx) ** 2 + (y - gy) ** 2)
            tg   = max(0.0, 1.0 - dist / (W * 0.54)) ** 2
            bg   = _lerp_color(bg, accent, tg * 0.14)

            # Zone 3 — subtle top-left brightness lift
            tl_d = math.sqrt(x ** 2 + y ** 2)
            ttl  = max(0.0, 1.0 - tl_d / (W * 0.56)) ** 1.5
            bg   = _lerp_color(bg, SURF0, ttl * 0.16)

            px[x, y] = bg

    return img


# ── Dot grid ──────────────────────────────────────────────────────────────────

def _draw_dot_grid(base_img: Image.Image, spacing: int = 36) -> Image.Image:
    """
    Render a uniform dot grid on a separate RGBA layer (opacity=50/255)
    so it reads as a subtle engineering-graph texture without competing with text.
    Dot radius is 1px.
    """
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    r = 1
    for y in range(0, H + spacing, spacing):
        for x in range(0, W + spacing, spacing):
            d.ellipse([x - r, y - r, x + r, y + r], fill=SURF1 + (50,))
    result = Image.alpha_composite(base_img.convert("RGBA"), layer)
    return result.convert("RGB")


# ── Ghost glyph ───────────────────────────────────────────────────────────────

def _draw_ghost_glyph(
    base_img: Image.Image,
    glyph:    str,
    accent:   tuple[int, int, int],
    font_size: int = 300,
    opacity:   int = 55,
) -> Image.Image:
    """
    Render a large monospace glyph as ghosted art in the right half.
    Anchored: right edge at W-80, vertically centered + 20px down.
    Hard left guard at x=690 — glyph will never intrude into the text zone.
    Opacity range 20-28 keeps it visible against the gradient without
    competing with any text element.
    """
    font  = ImageFont.truetype(FONT_BOLD, font_size)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d     = ImageDraw.Draw(layer)

    # Measure glyph
    tmp_d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bbox  = tmp_d.textbbox((0, 0), glyph, font=font)
    gw    = bbox[2] - bbox[0]
    gh    = bbox[3] - bbox[1]

    # Position
    gx = W - gw - 80 - bbox[0]
    gy = (H - gh) // 2 + 20 - bbox[1]

    # Enforce guard
    if gx < 690:
        gx = 690

    d.text((gx, gy), glyph, font=font, fill=accent + (opacity,))

    result = Image.alpha_composite(base_img.convert("RGBA"), layer)
    return result.convert("RGB")


# ── Geometric accent elements ─────────────────────────────────────────────────

def _draw_geometry(
    base_img: Image.Image,
    accent:   tuple[int, int, int],
) -> Image.Image:
    """
    Three accent geometry elements:

    1. Top-left L-bracket  — high opacity (200/255), 3px thick, 44px arms.
       Signals the content zone start; echoes a code editor's cursor chrome.

    2. Bottom-right inverse-L-bracket — medium opacity (70/255).
       Frames the domain text; creates compositional balance.

    3. Faint diagonal line — very low opacity (28/255).
       Runs from ~x=820 to off-canvas right, adds depth without
       drawing the eye away from the text.
    """
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d     = ImageDraw.Draw(layer)

    hi  = accent + (220,)
    mid = accent + (110,)
    lo  = accent + (50,)

    # Top-left L-bracket
    bx, by, blen, bthick = 56, 52, 44, 3
    d.rectangle([bx,          by,          bx + blen,   by + bthick], fill=hi)
    d.rectangle([bx,          by,          bx + bthick, by + blen  ], fill=hi)

    # Bottom-right inverse-L-bracket
    bx2, by2 = W - 56, H - 52
    d.rectangle([bx2 - blen, by2 - bthick, bx2, by2           ], fill=mid)
    d.rectangle([bx2 - bthick, by2 - blen, bx2, by2           ], fill=mid)

    # Faint diagonal
    d.line([(820, 0), (W + 50, int(H * 0.52))], fill=lo, width=1)

    result = Image.alpha_composite(base_img.convert("RGBA"), layer)
    return result.convert("RGB")


# ── Text utilities ────────────────────────────────────────────────────────────

def _wrap(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text into lines fitting within max_width pixels."""
    tmp  = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    words = text.split()
    lines: list[str] = []
    current: list[str] = []
    for word in words:
        test = " ".join(current + [word])
        bb   = tmp.textbbox((0, 0), test, font=font)
        if bb[2] - bb[0] > max_width and current:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines

def _fit_title(
    title:     str,
    max_width: int,
    max_lines: int = 2,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    """
    Return (font, lines, size) — largest font that wraps title into
    <= max_lines within max_width.  Falls back allowing 3 lines if needed.
    """
    for size in (88, 80, 72, 64, 56, 48):
        font  = ImageFont.truetype(FONT_BOLD, size)
        lines = _wrap(title, font, max_width)
        if len(lines) <= max_lines:
            return font, lines, size

    for size in (56, 48, 40, 36):
        font  = ImageFont.truetype(FONT_BOLD, size)
        lines = _wrap(title, font, max_width)
        if len(lines) <= 3:
            return font, lines, size

    font = ImageFont.truetype(FONT_BOLD, 32)
    return font, _wrap(title, font, max_width), 32

def _text_width(text: str, font: ImageFont.FreeTypeFont) -> int:
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    bb  = tmp.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0]


# ── Core generator ────────────────────────────────────────────────────────────

def generate_cover(
    slug:       str,
    title:      str,
    subtitle:   str,
    tags:       list[str],
    accent_hex: str,
    glyph:      str,
    out_path:   Path,
) -> None:
    """
    Full pipeline: make_background -> dot_grid -> ghost_glyph -> geometry
    No text is embedded — the visual identity comes entirely from accent color
    + glyph + geometry. Hugo renders title/description separately in the template.
    """
    accent = _hex_to_rgb(accent_hex)

    # ── Layer stack ────────────────────────────────────────────────────────────
    img = _make_background(accent)
    img = _draw_dot_grid(img)
    img = _draw_ghost_glyph(img, glyph, accent)
    img = _draw_geometry(img, accent)

    # ── Save ───────────────────────────────────────────────────────────────────
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, format="PNG", optimize=True)
    print(f"  PNG  {out_path}")


def generate_webp(png_path: Path) -> None:
    """Convert a PNG cover to WebP using cwebp or PIL fallback."""
    webp_path = png_path.with_suffix(".webp")
    try:
        result = subprocess.run(
            ["cwebp", "-q", "90", str(png_path), "-o", str(webp_path)],
            capture_output=True, check=True,
        )
        print(f"  WEBP {webp_path}")
    except (subprocess.CalledProcessError, FileNotFoundError):
        # PIL fallback
        img = Image.open(png_path)
        img.save(webp_path, format="WEBP", quality=90, method=6)
        print(f"  WEBP {webp_path}  (PIL fallback)")


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    args = sys.argv[1:]
    preview  = "--preview"  in args
    do_webp  = "--webp"     in args
    slugs    = [a for a in args if not a.startswith("--")]

    out_base = Path("/tmp/covers_preview") if preview else OUT_DIR
    out_base.mkdir(parents=True, exist_ok=True)

    targets = ARTICLES
    if slugs:
        targets = [a for a in ARTICLES if a[0] in slugs]
        if not targets:
            print(f"No matching articles for slugs: {slugs}")
            print(f"Available: {[a[0] for a in ARTICLES]}")
            sys.exit(1)

    print(f"Generating {len(targets)} cover(s) -> {out_base}")
    for slug, title, subtitle, tags, accent_hex, glyph in targets:
        png_path = out_base / f"{slug}.png"
        generate_cover(slug, title, subtitle, tags, accent_hex, glyph, png_path)
        if do_webp:
            generate_webp(png_path)

    print(f"\nDone. {len(targets)} cover(s) written.")
    if preview:
        print(f"Preview path: {out_base}")


if __name__ == "__main__":
    main()
