# ROADMAP — blog.jeromesoyer.fr

> Document de référence par phases. Mis à jour au fur et à mesure.
> Dernière mise à jour : 2026-03-09

---

## PHASE 1 — Foundation ✅ DONE

**Objectif : blog fonctionnel, design solide, contenu de base.**

| Tâche | Status |
|-------|--------|
| Setup Hugo + PaperMod | ✅ |
| CSS Catppuccin (Latte light / Mocha dark) | ✅ |
| i18n EN/FR (URLs séparées /fr/) | ✅ |
| Menus EN + FR | ✅ |
| Pages About EN + FR | ✅ |
| Pages Uses EN + FR | ✅ |
| Pages Search EN + FR | ✅ |
| Custom 404 terminal-style | ✅ |
| Favicon SVG | ✅ |
| OG image PNG 1200×630 | ✅ |
| Social icons (Strava, GitHub, Twitter, LinkedIn) | ✅ |
| Cloudflare Web Analytics | ✅ |
| Related posts (count: 3) | ✅ |
| Reading progress bar | ✅ |
| Mermaid.js lazy-load | ✅ |
| _index.md pour /posts/ EN+FR | ✅ |
| Article dotfiles EN+FR | ✅ |
| Article raycast-kitty EN+FR | ✅ |
| Cover images (1200×630, Catppuccin, 1 couleur/article) | ✅ |
| Publish 6 articles (nushell, modern-cli, kitty, chezmoi, neovim, rtk) | ✅ |
| CI/CD GitHub Actions → Cloudflare Pages | ✅ |

---

## PHASE 2 — SEO & Discoverabilité ✅ IN PROGRESS

**Objectif : être trouvé sur Google. Zero coût, impact maximal.**
**Agents utilisés : `seo-specialist`** — audit complet réalisé le 2026-03-09

| Tâche | Priorité | Status |
|-------|----------|--------|
| Soumettre sitemap Google Search Console | HIGH | ⬜ action manuelle requise |
| Vérifier domaine (DNS TXT Cloudflare) | HIGH | ⬜ action manuelle requise |
| Schema.org Article structured data (était vide !) | CRITICAL | ✅ Fix implémenté |
| Cover images dotfiles + raycast-kitty | HIGH | ✅ |
| Open Graph og:locale (en_US / fr_FR) | MEDIUM | ✅ Fix implémenté |
| Meta descriptions toutes les pages | HIGH | ✅ (about.md manquait) |
| hreflang x-default | MEDIUM | ✅ Ajouté |
| Title tags keyword-first (nushell, rtk) | MEDIUM | ✅ |
| Linking interne (clusters thématiques) | HIGH | ✅ 12 articles mis à jour |
| Fix stale refs (raycast "in review") | HIGH | ✅ about.md + about.fr.md |
| Canonical URLs vérification (EN/FR) | MEDIUM | ✅ OK natif PaperMod |
| robots.txt audit | LOW | ✅ OK natif |
| Pages tags avec descriptions | MEDIUM | ⬜ |
| Soumission Bing Webmaster Tools | LOW | ⬜ |
| Keyword cannibalization chezmoi/dotfiles | MEDIUM | ⬜ À surveiller |

### Actions manuelles restantes (Phase 2)
1. **Google Search Console** : ajouter propriété → vérifier via DNS TXT Cloudflare → soumettre `https://blog.jeromesoyer.fr/sitemap.xml`
2. **Rich Results Test** : valider Schema.org sur `https://search.google.com/test/rich-results`
3. **Bing Webmaster Tools** : soumettre sitemap (import automatique depuis GSC possible)

---

## PHASE 3 — Distribution & Cross-posting 📢

**Objectif : amplifier la portée sans créer de nouveau contenu.**
**Agents à utiliser : `content-marketer`, `Social Media Strategist`**

| Tâche | Priorité | Status |
|-------|----------|--------|
| Cross-post dev.to (canonical URL → garder SEO) | HIGH | ⬜ |
| Cross-post Hashnode | MEDIUM | ⬜ |
| Twitter/X automation (auto-tweet au publish) | MEDIUM | ⬜ |
| LinkedIn posts pour chaque article | MEDIUM | ⬜ |
| Soumission Hacker News (Show HN pour RTK) | HIGH | ⬜ |
| Soumission Reddit r/commandline, r/neovim, r/unixporn | HIGH | ⬜ |
| Newsletter setup (Buttondown — GDPR-friendly) | LOW | ⬜ |
| RSS améliorations (full content) | LOW | ⬜ |

---

## PHASE 4 — Contenu 📝

**Objectif : backlog d'articles et diversification.**
**Agents à utiliser : `content-creator`, `technical-writer`**

### Articles techniques à écrire

| Article | Langue | Priorité | Status |
|---------|--------|----------|--------|
| cv-pipeline (version HR-safe) | EN+FR | HIGH | ⬜ |
| HivePilot — personal CRM en Notion | EN+FR | HIGH | ⬜ |
| Aerospace + Sketchybar macOS setup | EN+FR | MEDIUM | ⬜ |
| Atuin self-hosted (Raspberry Pi) | EN+FR | MEDIUM | ⬜ |
| Framework Laptop + Fedora Atomic setup | EN+FR | MEDIUM | ⬜ |
| mise — remplacer nvm/rbenv/pyenv | EN+FR | MEDIUM | ⬜ |
| Wipey — pourquoi j'ai construit une app Swift | EN+FR | LOW | ⬜ |
| Paperless-ngx homelab setup | EN+FR | LOW | ⬜ |

### Articles non-tech (diversification)

| Article | Langue | Priorité | Status |
|---------|--------|----------|--------|
| Premier article running/Strava | EN+FR | MEDIUM | ⬜ |
| Setup cave à vin / wine tracker | FR | LOW | ⬜ |
| Ma vision sur le marché crypto | FR | LOW | ⬜ |

---

## PHASE 5 — Performance & Core Web Vitals ⚡

**Objectif : 100/100 Lighthouse. Pas critique mais bon pour le SEO.**
**Agents à utiliser : `performance-engineer`, `seo-specialist`**

| Tâche | Impact | Status |
|-------|--------|--------|
| Self-host Google Fonts (GDPR + perf) | HIGH | ⬜ |
| Optimisation images (WebP, lazy load) | HIGH | ⬜ |
| Mesure Core Web Vitals (LCP, CLS, FID) | HIGH | ⬜ |
| Réduire JS inutile (audit bundle) | MEDIUM | ⬜ |
| Preconnect hints pour CDN | LOW | ⬜ |
| PWA / service worker (offline) | LOW | ⬜ |
| Audit Lighthouse automatisé en CI | LOW | ⬜ |

---

## PHASE 6 — Engagement & Features Avancées 💬

**Objectif : garder les lecteurs, construire une communauté.**

| Tâche | Priorité | Status |
|-------|----------|--------|
| Commentaires giscus (GitHub Discussions) | MEDIUM | ⬜ |
| Temps de lecture estimé (déjà via PaperMod) | ✅ | ✅ |
| Partage social boutons (déjà désactivé, à reconsidérer) | LOW | ⬜ |
| Améliorer TOC (highlight section active) | MEDIUM | ⬜ |
| Back-to-top bouton amélioré | LOW | ⬜ |
| Mode "focus reading" (masquer nav au scroll) | LOW | ⬜ |
| Search améliorée (Pagefind ou Algolia) | LOW | ⬜ |

---

## Backlog / Idées

- Dark mode persist via localStorage (déjà géré par PaperMod)
- Statistiques de lecture publiques (type bearblog)
- Page projets dédiée (au lieu de About)
- Webmentions (interactions décentralisées)
- API posts (JSON) pour intégrations tierces

---

## Agents à mobiliser par phase

| Phase | Agents recommandés |
|-------|-------------------|
| SEO (P2) | `seo-specialist`, `research-analyst` |
| Distribution (P3) | `content-marketer`, `Social Media Strategist` |
| Contenu (P4) | `content-creator`, `technical-writer` |
| Performance (P5) | `performance-engineer`, `seo-specialist` |
| Features (P6) | `frontend-developer`, `ui-designer` |
