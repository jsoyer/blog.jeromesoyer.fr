---
title: "Engineering AI-First : L'Évolution de mes Dotfiles à 650+ Skills"
date: 2026-04-11T09:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Comment j'ai transformé mes dotfiles en une couche d'orchestration IA utilisant aictx, Yapee et plus de 600 skills personnalisés."
categories: ["DevOps", "AI", "Automation"]
tags: ["aictx", "claudecode", "opencode", "codex", "dotfiles", "yapee", "automation"]
cover:
  image: /images/covers/ai-first-engineering.webp
  alt: "AI-First Engineering"
---

### Le Terminal est le nouvel IDE
En ce début d'année 2026, la façon dont nous interagissons avec le code a changé pour toujours. Je ne passe plus le plus clair de mon temps à taper des caractères ; je le passe à **orchestrer du contexte**. Mes **[dotfiles](https://github.com/jsoyer/dotfiles)** ont évolué : de simples alias shell, ils sont devenus une **couche d'orchestration IA** complète.

C'est la "Least Privilege Life" appliquée à l'ingénierie : fournir exactement le bon contexte au bon outil, au bon moment.

### L'Écosystème : 190+ Agents, 650+ Skills
Mon environnement n'est plus un simple shell, c'est une usine. J'ai intégré trois outils CLI principaux, partageant tous un cerveau commun géré via mes dotfiles :

1.  **Claude Code :** Mon agent "Architecte" principal. Il gère l'analyse profonde du code et les refactorisations complexes.
2.  **OpenCode :** Une alternative rapide et extensible pour les tâches courantes et l'exécution de plugins via `ocx`.
3.  **Codex :** Intégré pour la génération directe de logique et l'intégration shell.

Le cœur de ce setup réside dans les répertoires `dot_claude/` et `dot_agents/`, qui hébergent désormais **192 agents spécialisés** et plus de **650 skills partagés**. Que je sois sous Fedora ou Windows, mes assistants IA ont les mêmes capacités et la même mémoire.

### Le Secret : `aictx`
La synchronisation est la partie la plus difficile d'un workflow IA multi-outils. C'est là qu'intervient **[`aictx`](https://github.com/jsoyer/dotfiles/releases/tag/aictx-v0.3.0) (v0.3.0)**.

Cet utilitaire agit comme une **Source de Vérité du Contexte**. Il gère l'état et l'historique entre mes différents CLIs, garantissant que si Claude prend une décision, OpenCode et Codex en soient informés. Fini les prompts répétés.

### Optimisation : RTK & Quality Gates
Pour éviter l'explosion du contexte et garder les coûts (et l'usage des tokens) sous contrôle, j'ai implémenté **RTK (Token Optimization Proxy)**.

Via des hooks d'événements personnalisés dans mes dotfiles, j'ai mis en place des **Quality Gates**. Avant qu'un agent puisse exécuter un changement majeur, il doit passer une validation gérée par un agent distinct. Ce "Moindre Privilège" pour l'exécution du code garantit que ma flotte d'IA ne dérive pas sur mon infrastructure.

### Le Résultat : Flow State 2.0
Avec ce setup, je n'utilise pas l'IA ; je **collabore** avec elle. En ayant mes skills et mes agents définis comme du code dans mes dotfiles, je peux configurer une nouvelle machine (comme mon récent cluster de Macs) et être pleinement productif avec mon workflow AI-First complet en moins de 5 minutes.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
ents définis comme du code dans mes dotfiles, je peux configurer une nouvelle machine (comme mon récent cluster de Macs) et être pleinement productif avec mon workflow AI-First complet en moins de 5 minutes.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
