---
title: "De Claude Max à SuperGrok Heavy : six mois au sommet, puis le grand saut"
date: 2026-08-22T09:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "Après des mois sur Claude Max 20x, j'ai basculé vers SuperGrok Heavy à 300 $/mois. Ce que ça change avec Cursor, Grok Build, Claude Code, RTK et 650+ skills."
categories: ["AI", "Productivity"]
tags: ["claude", "grok", "supergrok", "grok-build", "cursor", "ai", "productivity", "claudecode", "tokens", "agents"]
cover:
  image: /images/covers/claude-max-supergrok-heavy.webp
  alt: "Claude Max vers SuperGrok Heavy"
---

### Le contexte : je ne suis pas un utilisateur occasionnel

Quand Anthropic a lancé **Claude Max** en avril 2025, j'ai souscrit au tier **20x à 200 $/mois** sans hésiter. Pas par snobisme — par nécessité. Mon workflow décrit dans [Engineering AI-First](/fr/posts/ai-first-engineering/) ne tourne plus autour d'un seul outil : **Cursor** pour l'édition agentique et les refactors multi-fichiers, **Claude Code** pour l'exécution en terminal, OpenCode et Codex en soutien — le tout synchronisé via `aictx` et optimisé par **[RTK](/fr/posts/rtk/)**.

Sur une semaine type, je lance des dizaines de sessions **Cursor Agent** sur mes dotfiles, mes projets perso (HivePilot, cv-pipeline, RTK), et le travail chez Varonis. Quand le scope dépasse un repo ou qu'il faut enchaîner des commandes shell, je bascule sur Claude Code. Je tape rarement du code à la main ; j'orchestrre du contexte. Le tier Pro à 20 $/mois ? Un souvenir lointain. Max 5x ? Insuffisant après deux jours.

Pendant six mois, Claude Max a alimenté **Cursor et Claude Code** — mes deux interfaces principales vers les modôles Anthropic. Puis, en juillet 2026, j'ai fait quelque chose que je n'avais pas prévu : **j'ai annulé Max et souscrit à SuperGrok Heavy** — et découvert **Grok Build**, l'agent terminal de xAI qui change la donne côté CLI.

Voici pourquoi, ce que ça a changé dans Cursor et dans mon terminal, et si je le referais.

### Pourquoi Claude Max ne suffisait plus

Soyons honnêtes : Claude Max est un excellent produit. Les limites 20x par rapport à Pro, l'accès prioritaire aux nouveaux modèles, les sessions longues sans interruption — tout ça tient la route. Quand Opus 4 et les versions successives sont arrivées, j'étais dans la file prioritaire. Pour du refactoring profond, de l'analyse de code et de la rédaction technique, Claude reste difficile à battre.

Mais trois frustrations ont fini par s'accumuler :

**1. Le plafond de verre, même à 200 $/mois**

Les limites de session (fenêtre de 5 heures + quota hebdomadaire) sont documentées, mais la réalité quotidienne est plus frustrante. Un vendredi après-midi chargé, je me retrouvais bloqué en plein refactor sur mes dotfiles — exactement au moment où le flow était là. Pire : **Cursor Agent** consomme vite. Un agent qui explore un monorepo, lance des tests, itère sur un diff — ça peut vider un quota Max en une session. Max donne *beaucoup* plus que Pro, mais « beaucoup plus » n'est pas « illimité », et quand votre métier consiste à orchestrer des agents toute la journée dans Cursor *et* Claude Code, vous touchez le plafond plus souvent que vous ne l'admettez.

**2. Le raisonnement sur les problèmes vraiment durs**

Claude excelle sur le code, la prose et la structuration. Mais sur certains problèmes multi-étapes — architecture distribuée, analyse de benchmarks concurrents, raisonnement quantitatif — je sentais qu'il *convergeait trop vite*. Une réponse élégante, parfois trop tôt. J'avais envie d'un modèle qui **pense plus longtemps** avant de conclure.

**3. L'angle mort du temps réel**

Mon homelab, mes dashboards Grafana, Paperless — tout ça passe par MCP. Mais pour l'actualité tech, les annonces crypto, le sentiment du marché ou ce qui se dit *maintenant* sur un sujet, Claude dépend du web search, qui reste en retrait par rapport à ce que xAI peut faire avec **DeepSearch** et l'accès natif aux données X.

Ce n'était pas un problème tous les jours. C'était un problème les jours où ça comptait.

### Cursor : l'IDE qui a tout accéléré (et tout consommé)

Avant de parler de Grok, il faut être clair sur un point : **ce switch ne concerne pas Cursor**. Cursor est resté. C'est même devenu mon outil principal pour tout ce qui touche au code dans un dépôt.

J'ai longtemps été un puriste Neovim — mon [setup Neovim](/fr/posts/neovim-setup/) est toujours là, toujours configuré via chezmoi. Mais en 2025-2026, **Cursor a remplacé Neovim comme interface de travail par défaut** dès qu'un agent entre en jeu. Pas parce que l'éditeur est magique. Parce que l'intégration agent + diff + contexte repo est imbattable pour du travail multi-fichiers.

Concrètement, voici comment je répartis :

| Tâche | Outil | Pourquoi |
|---|---|---|
| Refactor multi-fichiers, PR, review de diff | **Cursor Agent** | Vision globale du repo, diffs inline, itération visuelle |
| Agents autonomes longue durée (Cloud Agents) | **Cursor** | Background agents qui tournent pendant que je fais autre chose |
| Scripts shell, CI, commandes enchaînées | **Claude Code** / **Grok Build** | Claude pour la prod ; Grok Build pour l'exploration |
| Édition rapide sans agent | **Neovim** | Toujours mon éditeur pour les micro-changements |

**Cursor Rules** font partie de mes dotfiles. Comme mes skills Claude Code, mes règles `.cursor/rules` voyagent avec chezmoi : conventions de code, garde-fous sécurité ([moindre privilège](/fr/posts/securing-ai-agents/)), instructions spécifiques par repo. Quand j'ouvre un projet sur une nouvelle machine, Cursor sait déjà comment je veux qu'il se comporte.

Les **serveurs MCP** que j'ai documentés dans [mon article Paperless](/fr/posts/mcp-servers/) tournent aussi dans Cursor. Même serveur, deux clients — Claude Code et Cursor Agent peuvent interroger mon archive Paperless sans réécrire l'intégration. C'est exactement la promesse de MCP, et Cursor en est l'un des meilleurs consommateurs.

Ce qui a changé avec le switch vers Grok Heavy, c'est la **séparation des contextes** :

- **Cursor** reste branché sur les modèles Anthropic (Opus, Sonnet) via mon abonnement Cursor + un tier Claude résiduel.
- **Grok Heavy** vit dans grok.com ou via l'API xAI — en dehors de Cursor, sans intégration native.

Résultat : quand je prépare un article de blog ou une analyse de marché, j'ouvre Grok dans le navigateur. Quand je code, je reste dans Cursor. **Deux fenêtres, deux modèles, zéro confusion.** C'est moins élégant qu'un tout-en-un, mais plus honnête sur ce que chaque outil fait bien.

Et oui — **cet article a été rédigé par un Cursor Cloud Agent**. Meta, mais révélateur : c'est exactement le genre de tâche où Cursor excelle (explorer un repo Hugo, générer du contenu, ouvrir une PR) pendant que Grok aurait été mon choix pour la réflexion initiale sur le sujet.

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
| **IDE agentique** | **Cursor** (Opus/Sonnet natifs) | Pas d'intégration Cursor native |
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

- **Claude Code** → repos de prod, permissions verrouillées, workflows `[moindre privilège](/fr/posts/securing-ai-agents/)` éprouvés
- **Grok Build** → exploration, prototypage, tâches où je veux le raisonnement Grok *dans* le terminal — refactors expérimentaux sur RTK, scripts d'infra, investigations multi-fichiers
- **RTK** → devant les deux, sans distinction

Le **Plan Mode** de Grok Build m'a particulièrement séduit sur les refactors risqués. Je lance `grok` en mode plan, je relis chaque étape, je commente ou réécris le plan avant qu'une seule ligne ne bouge. C'est le même réflexe de moindre privilège que mes Quality Gates — mais natif dans l'outil.

Les **subagents parallèles** changent aussi la donne sur les gros chantiers. Sur un refactor RTK qui touche parser, hooks et benchmarks, Grok Build délègue à des agents enfants en worktrees séparés. Pas aussi fluide que Cursor pour review visuelle des diffs, mais redoutable en terminal pur.

Et le **Agent Dashboard** (juin 2026) m'a rappelé les Cloud Agents de Cursor : plusieurs sessions Grok Build en parallèle, visibilité sur ce que chaque agent fait, réponse aux agents qui attendent une validation. Mon terminal est devenu une salle de contrôle.

**Les limites, honnêtement :**

- **256K tokens de contexte** — bien en deçà des 1M d'Opus. Sur un monorepo massif, ça se sent.
- **Beta encore instable** — j'ai eu des sessions qui ont dérivé sur des commandes shell non demandées. Mes garde-fous RTK et permissions restent non négociables.
- **Pas dans Cursor** — Grok Build vit au terminal. L'intégration ACP existe, mais ce n'est pas le même confort qu'un Cursor Agent avec diffs inline.

Mais le fait que xAI ait rendu Grok Build **compatible Claude Code par design** dit quelque chose sur le marché : la guerre ne se joue plus sur le format des skills, mais sur la qualité du modèle derrière. Et pour moi, avoir le choix entre Opus et Grok 4.6 *dans le même terminal setup* vaut une partie des 300 $/mois à eux seuls.

### Ce que j'ai perdu en quittant l'écosystème Anthropic

Je ne vais pas faire semblant : le switch a un coût réel au-delà des 100 $ supplémentaires.

**Cursor reste mon IDE agentique — mais sans Max derrière.** SuperGrok Heavy ne se branche pas nativement dans Cursor. Mon abonnement Cursor (Pro/Ultra) couvre une partie des requêtes agent, mais pour les sessions longues sur Opus, je ressens la différence depuis que Max n'alimente plus le robinet.

En revanche, **Grok Build comble une partie du fossé côté terminal**. Ce n'est pas Cursor, mais c'est un agent Grok natif qui comprend mon setup Claude Code — skills, MCP, hooks — sans friction. J'ai donc adopté un setup hybride à quatre niveaux :

- **Grok Heavy (web)** → réflexion, recherche, problèmes durs, DeepSearch
- **Grok Build (terminal)** → prototypage, exploration, tâches longues avec raisonnement Grok
- **Cursor** → édition agentique, refactors, PRs, Cloud Agents
- **Claude Code** → exécution terminal sur repos sensibles, CI, permissions verrouillées

Oui, ça veut dire payer **trois** abonnements (Cursor + Claude résiduel + Grok Heavy qui inclut Grok Build). Non, ce n'est pas rationnel sur le papier. Oui, c'est ce qui fonctionne.

**La qualité rédactionnelle.** Claude écrit mieux. Point. Mes articles passent encore par Claude (souvent via Cursor) pour la relecture et le polissage final. Grok est compétent, parfois plus direct, mais il manque cette *voix* — cette capacité à structurer une prose longue sans tomber dans le bullet-point générique.

**L'écosystème MCP.** Anthropic et Cursor ont une longueur d'avance côté IDE. Mais **Grok Build a rattrapé côté terminal** : mes [serveurs MCP Paperless](/fr/posts/mcp-servers/) tournent dans Claude Code, Cursor *et* Grok Build sans réécriture. Pour mon homelab agentique, le hub est désormais **Cursor + Claude Code + Grok Build** — trois clients, un seul serveur MCP.

**Les Artifacts.** Je les utilise moins qu'avant, mais quand j'en ai besoin — diagrammes, documents interactifs — Claude via Cursor ou claude.ai est imbattable. Grok n'a pas d'équivalent direct.

### RTK reste pertinent (peut-être plus qu'avant)

Ironie du sort : j'ai construit **[RTK](https://github.com/jsoyer/rtk)** pour économiser des tokens sur Claude Code et Cursor, et je l'utilise toujours — y compris quand je bascule vers Grok via l'API xAI. Un `git status` non proxifié brûle des tokens quel que soit le fournisseur, et **Cursor Agent** qui lance des commandes shell en boucle est un gouffre à tokens si vous ne filtrez pas l'output.

Avec trois abonnements premium, optimiser chaque token compte triple. Mes hooks RTK dans les dotfiles ne discriminent pas : `rtk git status` avant que l'output n'atteigne Cursor, Claude Code, Grok Build, ou n'importe quel modèle. Les économies de 60-90 % documentées dans mon article RTK restent valides, quel que soit le LLM en bout de chaîne.

### Le verdict après deux mois

**SuperGrok Heavy vaut-il 300 $/mois ?** Ça dépend de ce que vous optimisez.

- **Oui**, si vous faites de la recherche, de l'analyse multi-sources, du raisonnement sur des problèmes ouverts, ou si le temps réel est critique pour votre travail.
- **Non**, si votre usage principal est le code agentique dans **Cursor** ou le terminal avec Claude Code — dans ce cas, Max 20x (ou même 5x) reste le meilleur rapport qualité/prix.
- **Peut-être**, si vous êtes comme moi : un power user qui veut le meilleur des deux mondes et accepte de payer pour un setup hybride Cursor + Grok.

Mon setup actuel :

```
Réflexion / recherche / DeepSearch       →  SuperGrok Heavy (Grok 4 Heavy, grok.com)
Prototypage / exploration terminal       →  Grok Build (Grok 4.6, skills + MCP natifs)
Édition agentique / PRs / Cloud Agents   →  Cursor (Opus/Sonnet)
Repos sensibles / CI / permissions       →  Claude Code (tier Pro ou Max 5x)
Édition rapide sans agent                 →  Neovim
Optimisation tokens (tous)               →  RTK
```

Le coût total dépasse largement les 300 $/mois. C'est le prix d'être un early adopter qui refuse de choisir un seul camp — et qui ne veut surtout pas lâcher Cursor.

### Ce que ça dit sur le marché en 2026

Le parallèle avec l'histoire des IDE est frappant. On n'a plus « un outil IA » — on a un **stack IA**, comme on avait un stack de déploiement. **Cursor** pour l'édition agentique. **Grok Build** pour le terminal Grok. Claude Code pour l'exécution verrouillée. Grok Heavy pour le raisonnement profond. OpenCode pour la rapidité. RTK pour l'efficacité. `aictx` pour la cohérence.

Les éditeurs le savent. Anthropic pousse Max. xAI pousse Heavy. **Cursor** pousse les Cloud Agents et l'orchestration multi-modèles dans l'IDE. OpenAI a son tier Pro à 200 $. La course aux limites d'usage et aux modèles flagship ne ralentit pas.

Ma prédiction : d'ici fin 2026, la question ne sera plus « Claude ou Grok ? » mais « quel modèle pour quelle tâche, dans quel outil ? » — Cursor pour le code visuel, Grok Build pour le terminal, Grok Heavy pour la réflexion, et des abonnements qui n'ont toujours pas fusionné.

En attendant, je paie mes trois factures, j'optimise mes tokens avec RTK, et je continue à orchestrer du contexte dans Cursor plutôt qu'à taper du code.

---
*Stay local. Stay secure. Live the Least Privilege Life.*
