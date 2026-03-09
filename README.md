# blog.jeromesoyer.fr

Hugo blog — Catppuccin Mocha/Latte, PaperMod theme, EN/FR, deployed on Cloudflare Pages.

## Stack

- **Hugo** + PaperMod theme (submodule)
- **i18n** : EN (`/posts/`) + FR (`/fr/posts/`)
- **CI/CD** : GitHub Actions → Cloudflare Pages
- **Covers** : generated at build time via `scripts/generate_covers.py` (Pillow + JetBrains Mono)
- **Fonts** : self-hosted variable woff2 (Inter + JetBrains Mono)

---

## Écrire un nouvel article avec Claude

### Agents recommandés

| Besoin | Agent |
|--------|-------|
| Article technique (CLI, DevOps, code) | `technical-writer` |
| Article personnel / lifestyle | `content-marketer` |
| SEO — optimiser titre, meta, liens internes | `seo-specialist` |
| Relecture et amélioration du style | `editor` |

### Workflow complet

**1. Créer les fichiers Markdown**

```
content/posts/mon-article.md       # version EN
content/posts/mon-article.fr.md    # version FR
```

Front matter minimal à inclure :

```yaml
---
title: "Titre de l'article"
date: 2026-03-09T10:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Meta description SEO (150-160 caractères)"
categories: ["Tooling"]
tags: ["cli", "rust"]
cover:
  image: /images/covers/mon-article.webp
  alt: "Description de l'image"
---
```

**2. Ajouter la cover dans le script**

Ouvrir `scripts/generate_covers.py` et ajouter une entrée dans la liste `ARTICLES` :

```python
(
    "mon-article",            # slug = nom du fichier sans extension
    "Titre Court Percutant",  # max ~5 mots, vise 2 lignes à 88px
    "Sous-titre en une ligne.",
    ["Tag1", "Tag2"],         # 1 à 3 tags
    "#89b4fa",                # accent Catppuccin (voir palette ci-dessous)
    ">_",                     # glyph ghost (1-4 chars monospace)
),
```

Palette Catppuccin Mocha disponible :

| Couleur | Hex |
|---------|-----|
| Blue | `#89b4fa` |
| Green | `#a6e3a1` |
| Red | `#f38ba8` |
| Mauve | `#cba6f7` |
| Peach | `#fab387` |
| Yellow | `#f9e2af` |
| Teal | `#94e2d5` |
| Sky | `#89dceb` |
| Sapphire | `#74c7ec` |
| Pink | `#f5c2e7` |
| Lavender | `#b4befe` |
| Maroon | `#eba0ac` |

**3. Push**

```bash
git add content/posts/mon-article.md content/posts/mon-article.fr.md scripts/generate_covers.py
git commit -m "feat: add mon-article (EN+FR)"
git push
```

Le CI s'occupe du reste :
- génère la cover PNG + WebP automatiquement
- build Hugo
- déploie sur Cloudflare Pages

**C'est tout.** Pas besoin de générer les images localement.

---

## Régénérer les covers localement (optionnel)

```bash
# Toutes les covers
python3 scripts/generate_covers.py --webp

# Une seule cover
python3 scripts/generate_covers.py mon-article --webp

# Preview dans /tmp sans écraser les fichiers
python3 scripts/generate_covers.py mon-article --preview
```

Prérequis : `pip install Pillow` (les fonts sont dans `scripts/fonts/`).

---

## Publier un article

Le système de publication est **entièrement basé sur `draft`** dans le front matter.
Hugo n'inclut jamais les articles avec `draft: true` dans le build — c'est le seul interrupteur.

```
draft: true   → article invisible sur le site (même après push)
draft: false  → article live au prochain push
```

**Workflow :**

```bash
# 1. Écrire / relire sans publier — push librement, rien n'apparaît
git push   # draft: true → Hugo ignore l'article

# 2. Quand l'article est prêt : changer draft: true → draft: false
# puis commit + push → live en ~1 min
git add content/posts/mon-article.md content/posts/mon-article.fr.md
git commit -m "feat: publish mon-article"
git push
```

Pas besoin de branches, de tags git, ni de commandes spéciales. Le CI fait tout.

---

## Structure du repo

```
content/
  posts/          # articles (*.md EN, *.fr.md FR)
  tags/           # pages de taxonomie avec descriptions SEO
assets/
  css/extended/   # custom.css — Catppuccin + overrides PaperMod
layouts/
  partials/       # overrides Hugo : extend_head, extend_footer, schema, og
static/
  fonts/          # Inter + JetBrains Mono variable woff2 (self-hosted)
  images/covers/  # covers générées par CI (ne pas éditer manuellement)
scripts/
  generate_covers.py  # générateur de covers
  fonts/              # JetBrains Mono TTF (utilisé par le générateur)
```

---

## Variables d'environnement (GitHub Secrets)

| Secret | Usage |
|--------|-------|
| `CLOUDFLARE_API_TOKEN` | Deploy sur Cloudflare Pages |
| `CLOUDFLARE_ACCOUNT_ID` | ID du compte Cloudflare |
