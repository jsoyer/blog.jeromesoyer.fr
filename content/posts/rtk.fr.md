---
title: "RTK : Un proxy CLI Rust qui réduit la consommation de tokens LLM de 60-90%"
date: 2026-03-09T15:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Comment j'ai construit un proxy CLI en Rust qui réduit la consommation de tokens LLM de 60-90% sur les opérations dev courantes — et pourquoi c'est plus important qu'on ne le pense."
categories: ["Tooling", "AI"]
tags: ["rust", "cli", "llm", "claude", "ai", "productivity", "tokens", "automation"]
cover:
  image: /images/covers/rtk.webp
  alt: "RTK: Stop Burning Tokens"
---

Si vous utilisez Claude Code, Cursor, ou n'importe quel outil de dev assisté par IA au quotidien, voici un chiffre qui devrait vous déranger : **un seul `git status` sur un grand dépôt peut consommer plus de 10 000 tokens**. Pas parce que l'output est utile — mais parce que le texte brut est envoyé tel quel dans le contexte.

J'ai construit **[RTK](https://github.com/jsoyer/rtk)** (Rust Token Killer) pour régler ça. C'est un proxy CLI qui s'intercale entre vos commandes et votre LLM, filtrant et compressant l'output avant qu'il n'atteigne la fenêtre de contexte. Binaire Rust unique, zéro dépendance, 60-90% d'économies de tokens sur les opérations dev courantes.

### Le Problème

Regardez ce qui se passe quand vous lancez `git log --oneline` sur un dépôt avec 500 commits dans Claude Code : le LLM reçoit les 500 lignes. Il en a besoin de peut-être 10. Vous venez de brûler ~15 000 tokens pour du bruit.

Pareil avec `docker ps`, `npm list`, `ls -la` dans un répertoire chargé. Ces commandes produisent un output verbeux qui est surtout du bruit. L'IA n'a pas besoin du dump complet — elle a besoin d'un signal.

### Comment ça Marche

RTK agit comme un proxy transparent avec des filtres par commande :

```bash
# Sans RTK : output brut, coût token plein
git log --oneline  # 500 lignes → ~15k tokens

# Avec RTK : output filtré, compressé
rtk git log --oneline  # 20 dernières lignes + résumé → ~800 tokens
```

L'intégration par hook le rend complètement transparent — vous ne lancez jamais `rtk` directement après la configuration. Vos commandes existantes sont automatiquement réécrites.

### L'Analytique

La partie que je préfère : RTK trace tout.

```bash
rtk gain
# Rapport d'Économies de Tokens
# ─────────────────────────────────────
# Commandes proxifiées :     1 247
# Tokens économisés :        2 847 392
# Économie moyenne :         68,3%
# Meilleure perf: git log    94,1%
# ─────────────────────────────────────
# Coût économisé estimé :    ~8,54$

rtk discover
# Analyse votre historique Claude Code
# 47 commandes auraient pu être proxifiées
# Économies manquées estimées : 340 000 tokens
```

`rtk discover` est particulièrement utile — il parse votre historique de session Claude Code et vous dit quelles commandes vous avez lancées sans proxy et ce que vous auriez pu économiser.

### Pourquoi Rust ?

Binaire unique, zéro dépendance, overhead inférieur à la milliseconde. Le proxy doit être complètement invisible — s'il ajoute de la latence perceptible à vos commandes, vous arrêterez de l'utiliser. Rust a rendu la contrainte de performance triviale.

### La Vue d'Ensemble

Les coûts en tokens semblent abstraits jusqu'à ce que vous lanciez `rtk gain` après une semaine de Claude Code intensif et que vous voyiez que vous avez économisé 3 millions de tokens. Aux prix actuels de l'API, c'est de l'argent réel. Plus important encore, une fenêtre de contexte plus légère laisse plus de place au modèle pour ce qui compte vraiment : votre code, votre question, votre intention.

Les meilleurs outils sont ceux qui disparaissent. RTK tourne silencieusement en arrière-plan, et la seule fois où vous le remarquez, c'est quand vous consultez le rapport d'économies.

### Pour aller plus loin

Les filtres RTK sont conçus autour des sorties des outils modernes. Si vous ne les avez pas encore, voir [Les outils CLI modernes en 2026](/fr/posts/modern-cli-tools/).

---

**Code source** : [github.com/jsoyer/rtk](https://github.com/jsoyer/rtk)
