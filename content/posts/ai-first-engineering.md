---
title: "AI-First Engineering: My 650+ Skills Dotfiles Evolution"
date: 2026-04-11T09:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "How I transformed my dotfiles into an AI orchestration layer using aictx, Yapee, and over 600 custom skills."
categories: ["DevOps", "AI", "Automation"]
tags: ["aictx", "claudecode", "opencode", "codex", "dotfiles", "yapee", "automation"]
---

# [EN] AI-First Engineering: My 650+ Skills Dotfiles Evolution

### The Terminal is the New IDE
In early 2026, the way we interact with code changed forever. I no longer spend most of my time typing characters; I spend it **orchestrating context**. My **[dotfiles](https://github.com/jsoyer/dotfiles)** have evolved from simple shell aliases to a comprehensive **AI Orchestration Layer**.

This is the "Least Privilege Life" applied to engineering: providing exactly the right context to the right tool at the right time.

### The Ecosystem: 190+ Agents, 650+ Skills
My environment isn't just a shell; it's a factory. I've integrated three primary AI CLI tools, all sharing a common brain managed through my dotfiles:

1.  **Claude Code:** My primary "Architect" agent. It handles deep codebase analysis and complex refactoring.
2.  **OpenCode:** A fast, extensible alternative for quick tasks and specific plugin execution via `ocx`.
3.  **Codex:** Integrated for direct logic generation and shell integration.

The core of this setup lies in the `dot_claude/` and `dot_agents/` directories, which now host **192 specialized agents** and over **650 shared skills**. Whether I'm on Fedora or Windows, my AI assistants have the same capabilities and the same memory.

### The Secret Sauce: `aictx` & `Yapee`
Synchronization is the hardest part of multi-tool AI workflows. This is where two new projects in my ecosystem come in:

*   **[`aictx`](https://github.com/jsoyer/dotfiles/releases/tag/aictx-v0.3.0) (v0.3.0):** This utility acts as a **Context Source of Truth**. It manages the state and history between my different CLIs, ensuring that if Claude makes a decision, OpenCode and Codex are aware of it. No more repeated prompts.
*   **`Yapee`:** My automation handler. It connects my AI agents to my infrastructure. `Yapee` is the one triggering my **Synapse Forge** deployments or updating my **Homebrew Tap** when an agent finishes a build.

### Optimization: RTK & Quality Gates
To avoid "context bloat" and keep costs (and token usage) under control, I’ve implemented **RTK (Token Optimization Proxy)**. 

Through custom event hooks in my dotfiles, I’ve set up **Quality Gates**. Before an agent can execute a major change, it must pass a validation check handled by a separate agent. This "Least Privilege" for code execution ensures that my AI fleet doesn't go rogue on my infrastructure.

### The Result: Flow State 2.0
With this setup, I don't "use" AI; I **collaborate** with it. By having my skills and agents defined as code in my dotfiles, I can provision a new machine (like my recent Mac cluster) and be fully productive with my entire AI-First workflow in under 5 minutes.

---

# [FR] Engineering AI-First : L'Évolution de mes Dotfiles à 650+ Skills

### Le Terminal est le nouvel IDE
En ce début d'année 2026, la façon dont nous interagissons avec le code a changé pour toujours. Je ne passe plus le plus clair de mon temps à taper des caractères ; je le passe à **orchestrer du contexte**. Mes **[dotfiles](https://github.com/jsoyer/dotfiles)** ont évolué : de simples alias shell, ils sont devenus une **couche d'orchestration IA** complète.

C'est la "Least Privilege Life" appliquée à l'ingénierie : fournir exactement le bon contexte au bon outil, au bon moment.

### L'Écosystème : 190+ Agents, 650+ Skills
Mon environnement n'est plus un simple shell, c'est une usine. J'ai intégré trois outils CLI principaux, partageant tous un cerveau commun géré via mes dotfiles :

1.  **Claude Code :** Mon agent "Architecte" principal. Il gère l'analyse profonde du code et les refactorisations complexes.
2.  **OpenCode :** Une alternative rapide et extensible pour les tâches courantes et l'exécution de plugins via `ocx`.
3.  **Codex :** Intégré pour la génération directe de logique et l'intégration shell.

Le cœur de ce setup réside dans les répertoires `dot_claude/` et `dot_agents/`, qui hébergent désormais **192 agents spécialisés** et plus de **650 skills partagés**. Que je sois sous Fedora ou Windows, mes assistants IA ont les mêmes capacités et la même mémoire.

### Le Secret : `aictx` & `Yapee`
La synchronisation est la partie la plus difficile d'un workflow IA multi-outils. C'est là que deux nouveaux projets interviennent :

*   **[`aictx`](https://github.com/jsoyer/dotfiles/releases/tag/aictx-v0.3.0) (v0.3.0) :** Cet utilitaire agit comme une **Source de Vérité du Contexte**. Il gère l'état et l'historique entre mes différents CLIs, garantissant que si Claude prend une décision, OpenCode et Codex en soient informés. Fini les prompts répétés.
*   **`Yapee` :** Mon gestionnaire d'automatisation. Il connecte mes agents IA à mon infrastructure. `Yapee` est celui qui déclenche les déploiements sur ma **Forge Synapse** ou met à jour mon **Tap Homebrew** quand un agent termine un build.

### Optimisation : RTK & Quality Gates
Pour éviter l'explosion du contexte et garder les coûts (et l'usage des tokens) sous contrôle, j'ai implémenté **RTK (Token Optimization Proxy)**.

Via des hooks d'événements personnalisés dans mes dotfiles, j'ai mis en place des **Quality Gates**. Avant qu'un agent puisse exécuter un changement majeur, il doit passer une validation gérée par un agent distinct. Ce "Moindre Privilège" pour l'exécution du code garantit que ma flotte d'IA ne dérive pas sur mon infrastructure.

### Le Résultat : Flow State 2.0
Avec ce setup, je n'utilise pas l'IA ; je **collabore** avec elle. En ayant mes skills et mes agents définis comme du code dans mes dotfiles, je peux configurer une nouvelle machine (comme mon récent cluster de Macs) et être pleinement productif avec mon workflow AI-First complet en moins de 5 minutes.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
*Restez local. Restez en sécurité. Vivez la Least Privilege Life.*
