---
title: "De Claude Max à SuperGrok Heavy : six mois au sommet, puis le grand saut"
date: 2026-08-22T09:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "Après des mois sur Claude Max 20x, j'ai basculé vers SuperGrok Heavy à 300 $/mois. Herdr, Moshi, Grok Build, Grok Bot, Cursor Ultra — et l'app mobile Claude que je vais regretter."
categories: ["AI", "Productivity"]
tags: ["claude", "grok", "supergrok", "grok-build", "grok-bot", "cursor", "herdr", "moshi", "ai", "productivity", "claudecode", "tokens", "agents"]
cover:
  image: /images/covers/claude-max-supergrok-heavy.webp
  alt: "Claude Max vers SuperGrok Heavy"
---

### Le contexte : je ne suis pas un utilisateur occasionnel

Quand Anthropic a lancé **Claude Max** en avril 2025, j'ai souscrit au tier **20x à 200 $/mois** sans hésiter. Pas par snobisme — par nécessité. Mon workflow décrit dans [Engineering AI-First](/fr/posts/ai-first-engineering/) n'a jamais tourné autour d'un IDE graphique : c'est **la CLI, toujours la CLI**. **Claude Code** et **Grok Build** dans des panes **Herdr**, pilotés depuis le canapé via **Moshi** sur iPhone, synchronisés via `aictx` et orchestrés par **[HivePilot](/fr/posts/hivepilot/)**.

J'avais un petit abonnement **Cursor** — le plan de base, à peine utilisé. Pas par principe, par habitude : mon cerveau vit dans Kitty, mes agents vivent dans **Herdr**, et mon téléphone me sert de télécommande via **Moshi**. Je tape rarement du code à la main ; j'orchestrre du contexte.

Avec **SuperGrok Heavy**, tout a basculé : j'ai maintenant **Cursor Ultra**, et pour la première fois, Cursor sert à quelque chose — mais pas comme IDE.

Pendant six mois, Claude Max a alimenté **Claude Code, l'app mobile Claude, et mes sessions Herdr**. Puis, en juillet 2026, j'ai annulé Max et souscrit à SuperGrok Heavy — et découvert **Grok Build** dans mon terminal, puis **Grok Bot** sur mon iPhone.

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

### Herdr + Moshi : mon vrai workflow (Cursor en spectateur — jusqu'à Grok Bot)

Soyons clairs : **je n'ai jamais été un utilisateur Cursor au sens IDE**. J'avais le petit plan, j'ai testé l'édition agentique graphique, et je suis retourné au terminal. Ce n'est pas une critique — l'outil est excellent pour ceux qui vivent dans un IDE. Ce n'était tout simplement pas *mon* workflow.

Ça a changé avec **SuperGrok Heavy** — pas parce que j'ai soudainement adopté l'IDE, mais parce que Heavy débloque **Cursor Ultra** et **Grok Bot**. Mon abonnement Cursor dormant est devenu la porte d'entrée vers une couche d'agents que je n'avais pas : des collègues numériques avec leur propre ordinateur cloud, joignables depuis l'iPhone.

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
| IDE graphique / édition inline | **Cursor** | Ultra, mais quasi jamais pour coder — réservé à Grok Bot |
| Délégation autonome hors terminal | **Grok Bot** | Agents cloud 24/7, apps sans API, iOS natif |

Mes **skills**, hooks, plugins et serveurs **MCP** (Paperless, etc.) vivent dans mes dotfiles et fonctionnent dans Claude Code *et* Grok Build — peu importe le pane Herdr où je les lance. Herdr ne wrappe pas les agents ; il leur donne un **runtime persistant**. Moshi ne remplace pas le terminal ; il me donne une **fenêtre mobile** sur ce runtime.

Le soir, scénario typique : je lance trois agents dans Herdr sur mon Mac — un sur HivePilot, un sur mes dotfiles, un sur un article de blog. Je pars courir. Mon iPhone vibre via Moshi : l'agent HivePilot est `blocked`, il veut confirmer un `git push`. J'approuve depuis l'inbox Moshi sans rouvrir le laptop. C'est ça, mon workflow. Pas de diff inline dans un IDE — de l'orchestration terminal pure.

Ce qui a changé avec le switch vers Grok Heavy :

- **Grok Heavy (web/app)** → réflexion, DeepSearch, analyse temps réel
- **Grok Build** → nouveau pane Herdr, mêmes skills, modèle Grok
- **Grok Bot** → collègues autonomes sur iPhone, ordinateur cloud dédié
- **Cursor Ultra** → débloqué via Heavy, utilisé pour Grok Bot — pas pour l'IDE
- **Claude Code** → toujours là pour la prod et les permissions
- **Moshi** → inchangé pour le terminal ; Grok Bot prend le relais hors CLI

**Quatre interfaces, deux écosystèmes, un multiplexeur Herdr — et enfin un Cursor qui sert à quelque chose.**

*(Ironie : cet article a été rédigé par un Cursor Cloud Agent — via l'Ultra que je n'utilisais pas avant Heavy. Le cercle est bouclé.)*

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
| **Agents autonomes cloud** | — | **Grok Bot** (inclus Heavy + Ultra) |
| **Cursor** | Petit plan, inutilisé | **Ultra** (via Heavy, pour Grok Bot) |
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
- Mes **skills** dans `dot_claude/` et `dot_agents/` ? Reconnus.
- Mes hooks, plugins, serveurs **MCP** (Paperless, etc.) ? Reconnus.
- Mes règles de permission et conventions de repo ? Reconnues.

J'ai ouvert Grok Build dans mes dotfiles, et mon infrastructure agentique existante s'est branchée telle quelle. Pas de migration, pas de réécriture. Pour quelqu'un qui a investi des mois à câbler des [skills](/fr/posts/ai-first-engineering/), c'est le feature killer — pas Grok 4 Heavy en soi.

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
- **Grok Build** → exploration, prototypage, tâches où je veux le raisonnement Grok *dans* le terminal — refactors expérimentaux sur HivePilot, scripts d'infra, investigations multi-fichiers
- **HivePilot** → orchestration multi-agents au-dessus des deux, sans distinction

Le **Plan Mode** de Grok Build m'a particulièrement séduit sur les refactors risqués. Je lance `grok` en mode plan, je relis chaque étape, je commente ou réécris le plan avant qu'une seule ligne ne bouge. C'est le même réflexe de moindre privilège que mes Quality Gates — mais natif dans l'outil.

Les **subagents parallèles** changent aussi la donne sur les gros chantiers. Sur un refactor HivePilot qui touche orchestrateur, workers et benchmarks, Grok Build délègue à des agents enfants en worktrees séparés. Herdr affiche l'état de chaque pane dans la sidebar — `working`, `blocked`, `done` — sans que j'aie à scroller dans trois terminaux.

Et le **Agent Dashboard** de Grok Build (juin 2026) ressemble à ce que Herdr fait déjà nativement : plusieurs sessions en parallèle, visibilité sur ce que chaque agent fait, réponse aux agents qui attendent une validation. Mon multiplexeur est devenu une salle de contrôle — sauf que c'est Herdr qui orchestre, pas un IDE.

**Les limites, honnêtement :**

- **256K tokens de contexte** — bien en deçà des 1M d'Opus. Sur un monorepo massif, ça se sent.
- **Beta encore instable** — j'ai eu des sessions qui ont dérivé sur des commandes shell non demandées. Mes garde-fous HivePilot et permissions restent non négociables.
- **Pas d'équivalent Moshi** — Grok n'a pas de `moshi-hook`. Je peux piloter Grok Build depuis Moshi (c'est un vrai terminal), mais pas les notifications agent-aware, l'inbox unifiée, ni les approbations depuis le lock screen pour Grok comme pour Claude Code.

Mais le fait que xAI ait rendu Grok Build **compatible Claude Code par design** dit quelque chose sur le marché : la guerre ne se joue plus sur le format des skills, mais sur la qualité du modèle derrière. Et pour moi, avoir le choix entre Opus et Grok 4.6 *dans le même terminal setup* vaut une partie des 300 $/mois à eux seuls.

### Grok Bot : le collègue qui ne dort jamais

Si Grok Build a colonisé mon terminal, **Grok Bot** a colonisé ma poche — et c'est peut-être la surprise la plus marquante du switch.

Lancé en beta le 11 août 2026, **Grok Bot** n'est pas un chatbot. C'est une équipe d'**agents nommés et persistants**, chacun avec un job, une mémoire, et — point clé — **son propre ordinateur Linux dans le cloud**. Pas une chaîne d'appels API. Pas un serveur MCP à câbler. Un vrai navigateur, un vrai filesystem, un vrai terminal, qui tourne 24/7 même quand mon MacBook est fermé.

Inclus avec **SuperGrok Heavy** et **Cursor Ultra**. Connexion via compte Cursor — d'où l'intérêt soudain de mon abonnement Ultra, même sans ouvrir l'IDE.

**Comment ça marche concrètement :**

1. Je crée un Bot, je lui donne un nom et un rôle (« veille crypto », « tri emails Paperless », « prep article blog »).
2. Je lui envoie une tâche comme à un collègue — depuis l'app iOS ou le desktop.
3. Le Bot se connecte à mes outils (Gmail, Notion, interfaces web sans API) et exécute le workflow de bout en bout.
4. Il revient quand il a besoin d'une validation. Sinon, il livre.

**Ce qui le distingue de Grok Build et de Moshi :**

| | Grok Build | Moshi + Herdr | Grok Bot |
|---|---|---|---|
| **Où ça tourne** | Mon Mac / homelab | Mon Mac / homelab | Cloud xAI (ordi dédié) |
| **Interface** | Terminal (pane Herdr) | Terminal mobile SSH/Mosh | App iOS / desktop, messagerie |
| **Autonomie** | Session liée au host | Session liée au host | 24/7, laptop fermé |
| **Apps sans API** | Via MCP seulement | Via MCP seulement | Navigateur natif, login direct |
| **Parallélisme** | Subagents / panes Herdr | Panes Herdr | Bots multiples indépendants |
| **Mon usage** | Code, refactors, infra | Approbations, pilotage CLI | Veille, ops, tâches hors terminal |

Le cas d'usage qui m'a convaincu : la **veille article**. Avant, j'ouvrais l'app Claude mobile sur le RER pour brainstormer. Maintenant, je confie à un Grok Bot la veille crypto + tech du jour. Il scrape, synthétise, me laisse une note prête le matin. Je valide depuis l'iPhone. Mon laptop n'a pas bougé.

Autre cas : **ops sans MCP**. Paperless a un serveur MCP — parfait pour Claude Code dans Herdr. Mais beaucoup d'outils n'en ont pas. Grok Bot se connecte à l'interface web comme un humain. Pas élégant architecturalement ([moindre privilège](/fr/posts/securing-ai-agents/) ? discutable), mais redoutablement efficace pour les tâches ponctuelles.

**Le modèle « chief of staff »** fonctionne bien : un Bot coordinateur, des Bots spécialisés en dessous — veille, rédaction, monitoring homelab. Ils collaborent dans un thread, se passent le travail, et je ne suis plus le goulot d'étranglement.

**Les limites, honnêtement :**

- **Beta, et ça se sent** — des workflows dérivent, des logins expirent, des tâches restent bloquées sans notification claire.
- **Compte Cursor obligatoire** — xAI et Cursor sont désormais liés. Un abonnement de plus à suivre, même si Ultra vient avec Heavy.
- **Pas Linux desktop** — app macOS, Windows et iOS seulement. Mon homelab Fedora reste hors scope pour l'instant.
- **Privacy Mode** — les comptes en mode legacy doivent migrer vers le stockage cloud. À évaluer avec mon réflexe [moindre privilège](/fr/posts/securing-ai-agents/).

Mais Grok Bot comble un trou que ni Moshi ni Grok Build ne couvraient : **déléguer du vrai travail hors terminal, sans host allumé, depuis l'iPhone**. C'est la couche la plus proche de ce que l'app mobile Claude me donnait — sauf que le travail revient *fini*, pas en conversation.

### Ce que je regrette vraiment : l'app mobile Claude

Le switch vers Grok Heavy ne m'a pas fait regretter l'IDE Cursor — je ne l'utilisais déjà pas pour ça. Ce qui me manque *encore*, c'est **l'app mobile Claude** pour la conversation pure — brainstormer, résumer, dicter une idée sans déléguer une tâche.

Avec Claude Max, l'app iOS était mon interface de poche pour tout ce qui n'était pas du code : brainstormer un article, résumer un PDF, poser une question rapide en déplacement, dicter une idée entre deux réunions. Propre, rapide, synchronisée avec mon compte Max. Pas besoin d'SSH, pas besoin de Herdr, pas besoin de Moshi — juste Claude dans ma poche.

L'app Grok existe. Elle s'améliore. Mais aujourd'hui, elle n'offre pas la même fluidité pour le travail intellectuel quotidien hors terminal. Quand je suis dans le RER et que je veux affûter l'angle d'un article, j'ouvre Grok et... ça fait le job, sans la même *présence*. C'est subjectif, mais c'est le premier regret concret du switch.

**Grok Bot comble une partie du vide — mais pas tout.** Pour la délégation de tâches concrètes (veille, tri, prep), Grok Bot sur iOS est meilleur que tout ce que j'avais. Pour une conversation fluide sans objectif de livrable, l'app Claude reste en tête. Moshi, lui, reste irremplaçable pour piloter Herdr.

| Besoin | App Claude (avant) | Moshi + Herdr | Grok Bot (maintenant) | App Grok (maintenant) |
|---|---|---|---|---|
| Question rapide, rédaction | ✅ Natif, fluide | ❌ Overkill | ⚠️ Orienté tâche, pas chat | ⚠️ Correct, moins poli |
| Piloter un agent CLI en cours | ❌ | ✅ Inbox, push, approbations | ❌ | ❌ |
| Déléguer une tâche autonome | ❌ | ⚠️ Host allumé requis | ✅ 24/7, ordi cloud | ⚠️ Limité |
| Session longue autonome | ⚠️ Limité mobile | ✅ Agent tourne sur le host | ✅ Bot cloud indépendant | ⚠️ Web/app seulement |
| Apps sans API/MCP | ❌ | ❌ | ✅ Navigateur natif | ❌ |

Résultat : je garde probablement un **tier Claude Pro minimal** pour la conversation poche — même si Grok Bot prend le relais sur la délégation. Ironie : j'ai quitté Max pour économiser sur le quota terminal, et je paie désormais Heavy + Ultra + Claude Pro résiduel.

### Le reste de ce que j'ai perdu

Le switch a d'autres coûts au-delà des 100 $ supplémentaires et de l'app mobile.

**La qualité rédactionnelle.** Claude écrit mieux. Point. Mes articles passent encore par Claude pour la relecture et le polissage final — souvent depuis l'app mobile ou Claude Code dans un pane Herdr. Grok est compétent, parfois plus direct, mais il manque cette *voix*.

**L'écosystème MCP côté terminal.** **Grok Build a rattrapé** : mes [serveurs MCP Paperless](/fr/posts/mcp-servers/) tournent dans Claude Code et Grok Build sans réécriture, dans le même workspace Herdr. Pour mon homelab agentique, le hub est **Herdr + Claude Code + Grok Build** — deux agents, un multiplexeur, un Moshi.

**Les Artifacts.** Je les utilise moins qu'avant, mais quand j'en ai besoin — diagrammes, documents interactifs — Claude via claude.ai ou l'app mobile est imbattable. Grok n'a pas d'équivalent direct.

### HivePilot reste pertinent (peut-être plus qu'avant)

Ironie du sort : j'ai construit **[HivePilot](https://github.com/jsoyer/HivePilot)** pour orchestrer des swarms d'agents quand un seul modèle ne suffisait plus — et je l'utilise toujours. Claude Code dans un pane Herdr, Grok Build dans un autre, Grok Bot dans le cloud : **HivePilot** reste la couche qui décide *qui* fait *quoi*, pas le multiplexeur qui affiche l'état.

Avec SuperGrok Heavy + Cursor Ultra + un tier Claude résiduel, le risque n'est plus de manquer de tokens — c'est de lancer trop d'agents sans coordination. HivePilot ne discrimine pas le fournisseur : un worker Claude ou un worker Grok, c'est le même contrat.

### Le verdict après deux mois

**SuperGrok Heavy vaut-il 300 $/mois ?** Ça dépend de ce que vous optimisez.

- **Oui**, si vous faites de la recherche, de l'analyse multi-sources, du raisonnement sur des problèmes ouverts, ou si le temps réel est critique pour votre travail.
- **Non**, si votre usage principal est le terminal avec Claude Code — Max 20x (ou même 5x) reste le meilleur rapport qualité/prix.
- **Peut-être**, si vous êtes comme moi : workflow CLI Herdr/Moshi, Grok pour la réflexion, Claude résiduel pour la poche.

Mon setup actuel :

```
Réflexion / recherche / DeepSearch       →  SuperGrok Heavy (Grok 4 Heavy, grok.com)
Exploration / prototypage terminal       →  Grok Build (pane Herdr, skills + MCP natifs)
Délégation autonome / veille / ops       →  Grok Bot (iOS, ordi cloud, Cursor Ultra)
Repos sensibles / CI / permissions       →  Claude Code (pane Herdr, tier Pro résiduel)
Orchestration agents / sessions          →  Herdr (multiplexeur persistant)
Pilotage mobile terminal / approbations  →  Moshi + moshi-hook
Conversation rapide hors terminal        →  App Claude (tier Pro — à garder ?)
Édition rapide sans agent                 →  Neovim
Orchestration multi-agents               →  HivePilot
```

Le coût total dépasse largement les 300 $/mois — Heavy, Ultra, Claude Pro résiduel. C'est le prix d'un workflow CLI qui a fini par adopter Cursor — mais pour les Bots, pas pour l'éditeur.

### Ce que ça dit sur le marché en 2026

Le parallèle avec l'histoire des IDE est frappant — sauf que pour moi, l'IDE c'est le terminal. On n'a plus « un outil IA » — on a un **stack IA** : **Herdr** pour l'orchestration terminal, **Moshi** pour le pilotage mobile CLI, **Grok Build** et **Claude Code** pour l'exécution, **Grok Bot** pour la délégation cloud, **Grok Heavy** pour la réflexion, **Cursor Ultra** pour débloquer les Bots, **HivePilot** pour l'orchestration multi-agents, `aictx` pour la cohérence.

Les éditeurs le savent. Anthropic pousse Max — et une app mobile que je regrette encore pour le chat. xAI pousse Heavy, Grok Build, et Grok Bot. Cursor n'est plus juste un IDE : c'est l'infrastructure d'identité derrière les Bots. Herdr et Moshi comblent le fossé terminal que ni Cursor ni les apps natives ne couvrent seuls.

Ma prédiction : d'ici fin 2026, la question ne sera plus « Claude ou Grok ? » mais « quel modèle pour quelle surface ? » — terminal via Herdr, délégation via Grok Bot, pilotage via Moshi, réflexion via Grok Heavy — et des abonnements empilés (Heavy + Ultra + Pro) qui n'ont toujours pas fusionné.

En attendant, je paie mes factures, j'orchestre mes agents avec HivePilot, et je vérifie mon iPhone — Moshi pour les approbations CLI, Grok Bot pour la veille du matin, l'app Claude pour les questions qu'aucun Bot ne mérite.
