---
title: "De Claude Max à SuperGrok Heavy : six mois au sommet, puis le grand saut"
date: 2026-08-22T09:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "Après des mois sur Claude Max 20x, j'ai basculé vers SuperGrok Heavy à 300 $/mois. CLI Herdr, Moshi, Grok Build — et l'app mobile Claude que je vais regretter."
categories: ["AI", "Productivity"]
tags: ["claude", "grok", "supergrok", "grok-build", "herdr", "moshi", "ai", "productivity", "claudecode", "tokens", "agents"]
cover:
  image: /images/covers/claude-max-supergrok-heavy.webp
  alt: "Claude Max vers SuperGrok Heavy"
---

### Le contexte : je ne suis pas un utilisateur occasionnel

Quand Anthropic a lancé **Claude Max** en avril 2025, j'ai souscrit au tier **20x à 200 $/mois** sans hésiter. Pas par snobisme — par nécessité. Mon workflow décrit dans [Engineering AI-First](/fr/posts/ai-first-engineering/) n'a jamais tourné autour d'un IDE graphique : c'est **la CLI, toujours la CLI**. **Claude Code** et **Grok Build** dans des panes **Herdr**, pilotés depuis le canapé via **Moshi** sur iPhone, synchronisés via `aictx` et optimisés par **[RTK](/fr/posts/rtk/)**.

J'ai un abonnement Cursor sur un petit plan. Je ne l'utilise presque pas. Pas par principe — par habitude. Mon cerveau vit dans Kitty, mes agents vivent dans Herdr, et mon téléphone me sert de télécommande via Moshi. Je tape rarement du code à la main ; j'orchestrre du contexte. Le tier Pro à 20 $/mois ? Un souvenir lointain. Max 5x ? Insuffisant après deux jours.

Pendant six mois, Claude Max a alimenté **Claude Code, l'app mobile Claude, et mes sessions Herdr**. Puis, en juillet 2026, j'ai fait quelque chose que je n'avais pas prévu : **j'ai annulé Max et souscrit à SuperGrok Heavy** — et découvert **Grok Build**, l'agent terminal de xAI qui s'installe dans le même setup Herdr sans rien casser.

Voici pourquoi, ce que ça change dans mon terminal, et ce que je regrette déjà.

### Pourquoi Claude Max ne suffisait plus

Soyons honnêtes : Claude Max est un excellent produit. Les limites 20x par rapport à Pro, l'accès prioritaire aux nouveaux modèles, les sessions longues sans interruption — tout ça tient la route. Quand Opus 4 et les versions successives sont arrivées, j'étais dans la file prioritaire. Pour du refactoring profond, de l'analyse de code et de la rédaction technique, Claude reste difficile à battre.

Mais trois frustrations ont fini par s'accumuler :

**1. Le plafond de verre, même à 200 $/mois**

Les limites de session (fenêtre de 5 heures + quota hebdomadaire) sont documentées, mais la réalité quotidienne est plus frustrante. Un vendredi après-midi chargé, je me retrouvais bloqué en plein refactor sur mes dotfiles — exactement au moment où le flow était là. Pire : une session **Herdr** avec trois agents Claude Code en parallèle consomme vite. Un agent qui explore un monorepo, lance des tests, itère sur un diff — ça peut vider un quota Max en une session. Max donne *beaucoup* plus que Pro, mais « beaucoup plus » n'est pas « illimité », et quand votre métier consiste à orchestrer des agents toute la journée dans Herdr, vous touchez le plafond plus souvent que vous ne l'admettez.

**2. Le raisonnement sur les problèmes vraiment durs**

Claude excelle sur le code, la prose et la structuration. Mais sur certains problèmes multi-étapes — architecture distribuée, analyse de benchmarks concurrents, raisonnement quantitatif — je sentais qu'il *convergeait trop vite*. Une réponse élégante, parfois trop tôt. J'avais envie d'un modèle qui **pense plus longtemps** avant de conclure.

**3. L'angle mort du temps réel**

Mon homelab, mes dashboards Grafana, Paperless — tout ça passe par MCP. Mais pour l'actualité tech, les annonces crypto, le sentiment du marché ou ce qui se dit *maintenant* sur un sujet, Claude dépend du web search, qui reste en retrait par rapport à ce que xAI peut faire avec **DeepSearch** et l'accès natif aux données X.

Ce n'était pas un problème tous les jours. C'était un problème les jours où ça comptait.

### Herdr + Moshi : mon vrai workflow (pas Cursor)

Soyons clairs : **je ne suis pas un utilisateur Cursor**. J'ai un petit abonnement, j'ai testé, et je suis retourné au terminal. Ce n'est pas une critique de Cursor — l'outil est excellent pour ceux qui vivent dans un IDE graphique. Ce n'est tout simplement pas *mon* workflow.

Mon setup depuis le début de 2026, c'est **Herdr + Moshi** :

**[Herdr](https://herdr.dev)** est un multiplexeur terminal natif pour agents IA — pensez « tmux, mais il sait qu'un pane fait tourner Claude Code et qu'il est `working`, `blocked` ou `done` ». Mes agents tournent dans des panes Herdr persistantes sur mon MacBook ou mon homelab. Je ferme le capot, je me déconnecte en SSH, les agents continuent. Je réouvre Herdr, tout est là.

**[Moshi](https://getmoshi.app)** est le complément mobile : un terminal iOS conçu pour piloter des agents à distance via SSH/Mosh. Avec `moshi-hook` installé sur le host, j'ai les notifications push quand un agent attend une approbation, l'inbox unifiée pour Claude Code et Grok Build, et la dictée vocale on-device pour envoyer des prompts depuis le canapé. Herdr et Moshi sont faits l'un pour l'autre — Moshi détecte les workspaces Herdr et expose un panneau de raccourcis dédié.

Voici comment je répartis concrètement :

| Tâche | Outil | Pourquoi |
|---|---|---|
| Agents parallèles, sessions longues | **Herdr** + Claude Code / Grok Build | Panes persistantes, état agent visible, orchestration CLI |
| Pilotage mobile, approbations | **Moshi** + `moshi-hook` | Notifications, inbox, Mosh qui survit au réseau |
| Repos sensibles, permissions verrouillées | **Claude Code** | Workflows [moindre privilège](/fr/posts/securing-ai-agents/) éprouvés |
| Exploration, raisonnement Grok | **Grok Build** | Même skills, modèle différent, même pane Herdr |
| Édition rapide sans agent | **Neovim** | Toujours mon éditeur pour les micro-changements |
| IDE graphique agentique | **Cursor** | Abonné, quasi jamais ouvert |

Mes **650+ skills**, hooks, plugins et serveurs **MCP** (Paperless, etc.) vivent dans mes dotfiles et fonctionnent dans Claude Code *et* Grok Build — peu importe le pane Herdr où je les lance. Herdr ne wrappe pas les agents ; il leur donne un **runtime persistant**. Moshi ne remplace pas le terminal ; il me donne une **fenêtre mobile** sur ce runtime.

Le soir, scénario typique : je lance trois agents dans Herdr sur mon Mac — un sur RTK, un sur mes dotfiles, un sur un article de blog. Je pars courir. Mon iPhone vibre via Moshi : l'agent RTK est `blocked`, il veut confirmer un `git push`. J'approuve depuis l'inbox Moshi sans rouvrir le laptop. C'est ça, mon workflow. Pas de diff inline dans un IDE — de l'orchestration terminal pure.

Ce qui a changé avec le switch vers Grok Heavy :

- **Grok Heavy (web/app)** → réflexion, DeepSearch, analyse temps réel
- **Grok Build** → nouveau pane Herdr, mêmes skills, modèle Grok
- **Claude Code** → toujours là pour la prod et les permissions
- **Moshi** → inchangé, mais l'inbox ne parle plus qu'à moitié Claude

**Trois interfaces, deux écosystèmes, un seul multiplexeur Herdr.**

*(Ironie : cet article a été rédigé par un Cursor Cloud Agent — un outil que je n'utilise pas au quotidien. Preuve que le marché des agents se joue aussi hors du terminal, même pour les puristes CLI.)*

### SuperGrok Heavy : ce que 300 $/mois achètent vraiment

xAI a lancé **SuperGrok Heavy** le 9 juillet 2025 à **300 $/mois** — soit 50 % de plus que Claude Max 20x. Le positionnement est clair : ce n'est pas pour tout le monde. C'est le tier « si le raisonnement est votre produit ».

Ce que j'ai obtenu en échange :

| | Claude Max 20x | SuperGrok Heavy |
|---|---|---|
| **Prix** | 200 $/mois | 300 $/mois |
| **Modèle phare** | Claude Opus (accès prioritaire) | Grok 4 Heavy (multi-agent) |
| **Raisonnement** | Excellent, rapide | Parallèle, plus lent, souvent plus profond |
| **Contexte** | Très large (selon modèle) | 256K tokens |
| **Temps réel** | Web search | DeepSearch + données X natives |
| **Écosystème dev** | Claude Code, Cowork, MCP mature | Grok Build, API xAI |
| **Mobile** | **App Claude** (Max) + Moshi | App Grok (moins mature) |
| **Multiplexeur agents** | Herdr | Herdr (inchangé) |
| **Agent terminal** | Claude Code | **Grok Build** (inclus SuperGrok) |
| **Limites d'usage** | Session 5h + quota hebdo | Pool hebdomadaire (plus généreux) |

Le différenciateur, c'est **Grok 4 Heavy** : un modèle multi-agent qui lance plusieurs chaînes de raisonnement en parallèle et synthétise le résultat. Sur papier, ça ressemble à du marketing. En pratique, sur un problème d'architecture ou une analyse comparative de quatre approches techniques, la différence est perceptible — pas toujours « meilleure », mais **différente**. Grok explore des angles que Claude écarte parfois trop vite.

**DeepSearch** a été le deuxième argument décisif. Quand je prépare un article de blog, une veille crypto ou une analyse de tendance IA, pouvoir croiser recherche web, posts X récents et synthèse en une seule session change la donne. Ce n'est pas magique — le bruit sur X est réel — mais pour capter le *signal* d'un sujet en mouvement, c'est nettement plus efficace que mes anciens workflows.

### Grok Build : le plot twist terminal

Si SuperGrok Heavy m'a fait franchir le pas, **Grok Build** m'a fait rester.

Lancé en beta le 25 mai 2026, **Grok Build** est l'agent de code terminal de xAI — un CLI en Rust avec TUI plein écran, alimenté aujourd'hui par **Grok 4.6**. Une ligne pour installer :

```bash
curl -fsSL https://x.ai/cli/install.sh | bash
```

Inclus dans l'abonnement SuperGrok (et donc Heavy). Et là, xAI a fait quelque chose de malin : **Grok Build est compatible avec l'écosystème Claude Code sans configuration**.

Concrètement, dans mon repo :

- Mon `AGENTS.md` ? Reconnu.
- Mes **650+ skills** dans `dot_claude/` et `dot_agents/` ? Reconnus.
- Mes hooks, plugins, serveurs **MCP** (Paperless, etc.) ? Reconnus.
- Mes règles de permission et conventions de repo ? Reconnues.

J'ai ouvert Grok Build dans mes dotfiles, et mon infrastructure agentique existante s'est branchée telle quelle. Pas de migration, pas de réécriture. Pour quelqu'un qui a investi des mois à câbler [650+ skills](/fr/posts/ai-first-engineering/), c'est le feature killer — pas Grok 4 Heavy en soi.

**Ce que Grok Build apporte en plus de Claude Code :**

| Capacité | Grok Build | Claude Code |
|---|---|---|
| **Plan Mode** | Plan structuré, édition bloquée jusqu'à approbation | Plan mode similaire, plus mature |
| **Subagents parallèles** | Délégation native, worktrees dédiés | Subagents, intégration worktree en progrès |
| **Tâches longues** | `/goal` pour exécution autonome prolongée | Sessions longues, limites quota |
| **Headless / CI** | `grok -p "prompt"` avec output JSON | `claude -p` équivalent |
| **Intégration IDE** | ACP via `grok agent stdio` | Natif dans plusieurs éditeurs |
| **Modèle** | Grok 4.6 (raisonnement xAI) | Opus/Sonnet (Anthropic) |
| **Open source** | [xai-org/grok-build](https://github.com/xai-org/grok-build) depuis juillet 2026 | Fermé |

En pratique, voici comment je répartis le terminal aujourd'hui :

- **Claude Code** → repos de prod, permissions verrouillées, workflows [moindre privilège](/fr/posts/securing-ai-agents/) éprouvés
- **Grok Build** → exploration, prototypage, tâches où je veux le raisonnement Grok *dans* le terminal — refactors expérimentaux sur RTK, scripts d'infra, investigations multi-fichiers
- **RTK** → devant les deux, sans distinction

Le **Plan Mode** de Grok Build m'a particulièrement séduit sur les refactors risqués. Je lance `grok` en mode plan, je relis chaque étape, je commente ou réécris le plan avant qu'une seule ligne ne bouge. C'est le même réflexe de moindre privilège que mes Quality Gates — mais natif dans l'outil.

Les **subagents parallèles** changent aussi la donne sur les gros chantiers. Sur un refactor RTK qui touche parser, hooks et benchmarks, Grok Build délègue à des agents enfants en worktrees séparés. Herdr affiche l'état de chaque pane dans la sidebar — `working`, `blocked`, `done` — sans que j'aie à scroller dans trois terminaux.

Et le **Agent Dashboard** de Grok Build (juin 2026) ressemble à ce que Herdr fait déjà nativement : plusieurs sessions en parallèle, visibilité sur ce que chaque agent fait, réponse aux agents qui attendent une validation. Mon multiplexeur est devenu une salle de contrôle — sauf que c'est Herdr qui orchestre, pas un IDE.

**Les limites, honnêtement :**

- **256K tokens de contexte** — bien en deçà des 1M d'Opus. Sur un monorepo massif, ça se sent.
- **Beta encore instable** — j'ai eu des sessions qui ont dérivé sur des commandes shell non demandées. Mes garde-fous RTK et permissions restent non négociables.
- **Pas d'équivalent Moshi** — Grok n'a pas de `moshi-hook`. Je peux piloter Grok Build depuis Moshi (c'est un vrai terminal), mais pas les notifications agent-aware, l'inbox unifiée, ni les approbations depuis le lock screen pour Grok comme pour Claude Code.

Mais le fait que xAI ait rendu Grok Build **compatible Claude Code par design** dit quelque chose sur le marché : la guerre ne se joue plus sur le format des skills, mais sur la qualité du modèle derrière. Et pour moi, avoir le choix entre Opus et Grok 4.6 *dans le même terminal setup* vaut une partie des 300 $/mois à eux seuls.

### Ce que je regrette vraiment : l'app mobile Claude

Le switch vers Grok Heavy ne m'a pas fait regretter Cursor — je ne l'utilisais déjà pas. Ce qui me manque *déjà*, c'est **l'application mobile Claude**.

Avec Claude Max, l'app iOS était mon interface de poche pour tout ce qui n'était pas du code : brainstormer un article, résumer un PDF, poser une question rapide en déplacement, dicter une idée entre deux réunions. Propre, rapide, synchronisée avec mon compte Max. Pas besoin d'SSH, pas besoin de Herdr, pas besoin de Moshi — juste Claude dans ma poche.

L'app Grok existe. Elle s'améliore. Mais aujourd'hui, elle n'offre pas la même fluidité pour le travail intellectuel quotidien hors terminal. Quand je suis dans le RER et que je veux affûter l'angle d'un article, j'ouvre Grok et... ça fait le job, sans la même *présence*. C'est subjectif, mais c'est le premier regret concret du switch.

**Moshi comble une partie du vide — mais pas tout.** Moshi me reconnecte à mes agents Herdr depuis l'iPhone : approbations, inbox, sessions longues. C'est génial pour *piloter* du code à distance. Ce n'est pas la même chose qu'une conversation Claude sur le canapé sans terminal sous-jacent. Deux usages différents :

| Besoin | App Claude (avant) | Moshi + Herdr (maintenant) | App Grok (maintenant) |
|---|---|---|---|
| Question rapide, rédaction | ✅ Natif, fluide | ❌ Overkill | ⚠️ Correct, moins poli |
| Piloter un agent en cours | ❌ | ✅ Inbox, push, approbations | ❌ Pas de hook équivalent |
| Session longue autonome | ⚠️ Limité mobile | ✅ Agent tourne sur le host | ⚠️ Web/app seulement |
| Hors réseau / sans laptop | ✅ | ⚠️ Besoin du host allumé | ✅ |

Résultat : je garde probablement un **tier Claude Pro minimal** rien que pour l'app mobile — même si mon terminal est passé à Grok. Ironie : j'ai quitté Max pour économiser sur le quota terminal, et je risque de repayer Anthropic pour la poche.

### Le reste de ce que j'ai perdu

Le switch a d'autres coûts au-delà des 100 $ supplémentaires et de l'app mobile.

**La qualité rédactionnelle.** Claude écrit mieux. Point. Mes articles passent encore par Claude pour la relecture et le polissage final — souvent depuis l'app mobile ou Claude Code dans un pane Herdr. Grok est compétent, parfois plus direct, mais il manque cette *voix*.

**L'écosystème MCP côté terminal.** **Grok Build a rattrapé** : mes [serveurs MCP Paperless](/fr/posts/mcp-servers/) tournent dans Claude Code et Grok Build sans réécriture, dans le même workspace Herdr. Pour mon homelab agentique, le hub est **Herdr + Claude Code + Grok Build** — deux agents, un multiplexeur, un Moshi.

**Les Artifacts.** Je les utilise moins qu'avant, mais quand j'en ai besoin — diagrammes, documents interactifs — Claude via claude.ai ou l'app mobile est imbattable. Grok n'a pas d'équivalent direct.

### RTK reste pertinent (peut-être plus qu'avant)

Ironie du sort : j'ai construit **[RTK](https://github.com/jsoyer/rtk)** pour économiser des tokens sur Claude Code et Grok Build dans Herdr, et je l'utilise toujours. Un `git status` non proxifié brûle des tokens quel que soit le fournisseur, et un agent qui lance des commandes shell en boucle dans un pane Herdr est un gouffre à tokens si vous ne filtrez pas l'output.

Avec SuperGrok Heavy + un tier Claude résiduel pour l'app mobile, optimiser chaque token compte double. Mes hooks RTK dans les dotfiles ne discriminent pas : `rtk git status` avant que l'output n'atteigne Claude Code, Grok Build, ou n'importe quel modèle.

### Le verdict après deux mois

**SuperGrok Heavy vaut-il 300 $/mois ?** Ça dépend de ce que vous optimisez.

- **Oui**, si vous faites de la recherche, de l'analyse multi-sources, du raisonnement sur des problèmes ouverts, ou si le temps réel est critique pour votre travail.
- **Non**, si votre usage principal est le terminal avec Claude Code — Max 20x (ou même 5x) reste le meilleur rapport qualité/prix.
- **Peut-être**, si vous êtes comme moi : workflow CLI Herdr/Moshi, Grok pour la réflexion, Claude résiduel pour la poche.

Mon setup actuel :

```
Réflexion / recherche / DeepSearch       →  SuperGrok Heavy (Grok 4 Heavy, grok.com)
Exploration / prototypage terminal       →  Grok Build (pane Herdr, skills + MCP natifs)
Repos sensibles / CI / permissions       →  Claude Code (pane Herdr, tier Pro résiduel)
Orchestration agents / sessions          →  Herdr (multiplexeur persistant)
Pilotage mobile / approbations           →  Moshi + moshi-hook
Conversation rapide hors terminal        →  App Claude (tier Pro — à garder ?)
Édition rapide sans agent                 →  Neovim
Optimisation tokens (tous)               →  RTK
```

Le coût total dépasse largement les 300 $/mois — surtout si je garde Claude Pro pour l'app mobile. C'est le prix d'un workflow CLI qui refuse de choisir un seul camp.

### Ce que ça dit sur le marché en 2026

Le parallèle avec l'histoire des IDE est frappant — sauf que pour moi, l'IDE c'est le terminal. On n'a plus « un outil IA » — on a un **stack IA** : **Herdr** pour l'orchestration, **Moshi** pour le mobile, **Grok Build** et **Claude Code** pour l'exécution, **Grok Heavy** pour la réflexion, **RTK** pour l'efficacité, `aictx` pour la cohérence.

Les éditeurs le savent. Anthropic pousse Max — et une app mobile que je regrette déjà. xAI pousse Heavy et Grok Build. Herdr et Moshi comblent le fossé que ni Cursor ni les apps natives ne couvrent pour les puristes CLI.

Ma prédiction : d'ici fin 2026, la question ne sera plus « Claude ou Grok ? » mais « quel modèle pour quelle surface ? » — terminal via Herdr, poche via l'app native ou Moshi, réflexion via Grok Heavy — et des abonnements qui n'ont toujours pas fusionné.

En attendant, je paie mes factures, j'optimise mes tokens avec RTK, et je vérifie mon iPhone toutes les cinq minutes pour voir si Moshi a quelque chose — en espérant qu'un jour l'app Grok rattrape l'app Claude.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
