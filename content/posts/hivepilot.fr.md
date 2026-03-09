---
title: "HivePilot : Construire un système d'orchestration multi-agents de A à Z"
date: 2026-02-05T09:30:00+01:00
draft: true
author: "Jerome Soyer"
description: "Comment j'ai construit un système d'orchestration multi-agents en 2024 quand les outils n'existaient pas. Ce qui a marché, ce qui a explosé, et pourquoi les swarms d'agents sont plus difficiles qu'on ne le pense."
categories: ["Engineering", "AI"]
tags: ["ai", "automation", "llm", "agents", "productivity", "python", "engineering"]
cover:
  image: /images/covers/hivepilot.webp
  alt: "HivePilot Multi-Agent System"
---

À partir du moment où tu réalises qu'un seul LLM ne suffit pas, tu construis des systèmes multi-agents. Tu ne choisis pas de le faire — tu te retrouves juste là.

J'ai construit **[HivePilot](https://github.com/jsoyer/HivePilot)** fin 2024, quand les frameworks multi-agents étaient surtout théoriques. Le problème était simple : certaines tâches sont trop complexes pour qu'un seul modèle les nail, mais parfaites pour un swarm d'agents spécialisés. Code review automation, génération de docs, integration testing — tout ça a besoin d'angles différents.

Voici ce que j'ai appris sur l'orchestration d'agents, pourquoi c'est plus difficile que ça n'y parait, et où tout a failli s'écrouler.

### Le Problème Qu'Un Seul Agent Peut Pas Résoudre

Imagine : tu veux un système IA qui review automatiquement tes PRs, flag les issues, suggère des améliorations, et génère la doc pour les nouveaux fichiers.

Un seul LLM peut le faire. Il va lire la PR, checker la logique, suggérer des trucs. Mais il va manquer des choses :
- Des edge cases qui ont besoin de connaissance spécialisée
- Des vulnérabilités de sécurité qui nécessitent du threat modeling
- Des régressions de performance qui ont besoin de contexte de benchmarking
- De la doc qui a besoin à la fois de précision technique et de lisibilité

Tu *pourrais* prompt engineer ton chemin autour de ça. Ajouter 40 instructions de plus, du contexte, des exemples, des feedback loops.

Ou tu pourrais faire ce que j'ai fait : construire une hive.

### Architecture HivePilot

Le concept core est simple : **les agents sont des workers, l'orchestrateur est le boss**.

```
┌─────────────────────────────────┐
│     Central Orchestrator         │
│  (Manages state, routing, flow)  │
└────────┬────────────┬────────────┘
         │            │
    ┌────▼──┐    ┌────▼──┐
    │CodeBot│    │DocBot  │     Chaque agent est
    │       │    │        │     spécialisé pour
    └───────┘    └────────┘     un job
    ┌──────┐    ┌────────┐
    │SecBot│    │TestBot │
    │      │    │        │
    └──────┘    └────────┘
```

L'orchestrateur fonctionne comme ça :

```python
# Logique simplifiée de l'orchestrateur HivePilot
class Hive:
    def __init__(self):
        self.agents = {
            "code_reviewer": CodeReviewAgent(),
            "security": SecurityAgent(),
            "docs": DocumentationAgent(),
            "performance": PerformanceAgent(),
            "tests": TestAgent(),
        }
        self.state = HiveState()

    def process_pr(self, pr_data):
        # Phase 1: Parse la PR
        self.state.pr = parse_pr(pr_data)

        # Phase 2: Dispatch vers les agents en parallèle
        results = {}
        for agent_name, agent in self.agents.items():
            results[agent_name] = agent.analyze(
                self.state.pr,
                context=self.state.context
            )

        # Phase 3: Agrège les findings
        return self.aggregate_findings(results)
```

Chaque agent opère indépendamment mais partage l'état. L'orchestrateur route le travail, gère les dépendances, et agrège les findings.

### Les Challenges Qui Ont Failli Me Briser

**1. Le State Management est Fou**

Le premier problème : les agents ont besoin de voir le même code mais arrivent à des conclusions différentes. Si le CodeBot analyse une fonction et la marque comme "besoin de refactoring", le SecurityBot a besoin de le savoir pour ne pas passer du temps sur du code déjà flaggé.

Mais les agents ont aussi besoin d'indépendance. Si un agent crash, les autres continuent.

```python
# La solution : des snapshots d'état immutable
@dataclass
class HiveState:
    pr_data: Dict  # PR originale (immutable)
    context: Dict  # Contexte partagé
    findings: Dict[str, List[Finding]]  # Findings par agent

    def get_snapshot_for_agent(self, agent_name):
        """Chaque agent reçoit une copie read-only de l'état"""
        return HiveStateSnapshot(
            pr_data=deepcopy(self.pr_data),
            context=deepcopy(self.context),
            previous_findings=self.findings  # Read-only
        )
```

**2. Les Agents Se Disputent**

C'est arrivé. SecurityBot flag un pattern comme une vulnérabilité. CodeBot review le même code et dit "non, c'est bon, c'est un pattern courant."

Ils appellent tous les deux l'orchestrateur avec des findings conflictants. Maintenant quoi?

J'ai ajouté une phase de "résolution de conflits" :

```python
def resolve_conflicts(self, findings_dict):
    """Quand les agents sont en désaccord, demande-leur de justifier"""
    conflicts = self.detect_conflicts(findings_dict)

    for conflict in conflicts:
        # Re-run les deux agents avec conscience explicite du conflit
        agent1_result = conflict.agent1.re_evaluate(
            conflict.item,
            disagreement_with=conflict.agent2.name,
            agent2_rationale=conflict.agent2_reason
        )

        agent2_result = conflict.agent2.re_evaluate(
            conflict.item,
            disagreement_with=conflict.agent1.name,
            agent1_rationale=conflict.agent1_reason
        )

        # Accepte celui qui a la confiance + l'evidence la plus forte
        return self.pick_stronger_finding(agent1_result, agent2_result)
```

C'est pas parfait mais ça réduit les hallucinations.

**3. Les Boucles Infinies**

Un agent envoie un finding. L'orchestrateur le route à un autre agent pour vérification. Cet agent envoie une question de suivi. Le premier agent répond. Le deuxième agent remet en question la réponse.

Avant que tu le saches, tu as 47 messages agent-to-agent et tu brûles des tokens comme si c'était une free tier d'API LLM.

```python
# Solution : max depth + decision timeout
class AgentMessage:
    content: str
    depth: int  # Track conversation depth
    timestamp: float

def route_message(self, message, max_depth=3):
    if message.depth >= max_depth:
        # Force resolution : escalade à l'orchestrateur
        return self.orchestrator_decides(message)

    # Aussi timeout : si la chaîne de messages prend > 30 secondes, force resolution
    if time.time() - message.timestamp > 30:
        return self.orchestrator_decides(message)

    return self.route_to_next_agent(message)
```

**4. Un Agent Crash, Tout Ralentit**

Si CodeBot prend 45 secondes à répondre et les autres finissent en 2 secondes, tu attends 45 secondes pour le résultat complet.

J'ai ajouté des timeouts d'agent et des stratégies de fallback :

```python
async def wait_for_agents(self, agent_tasks, timeout=10):
    """Gather results avec timeouts"""
    results = {}

    try:
        done, pending = await asyncio.wait(
            agent_tasks.values(),
            timeout=timeout,
            return_when=asyncio.FIRST_EXCEPTION
        )

        for agent_name, task in agent_tasks.items():
            if task.done():
                results[agent_name] = task.result()
            else:
                # Agent a timeout — use fallback
                results[agent_name] = self.fallback_analysis(agent_name)

    except Exception as e:
        results["error"] = str(e)

    return results
```

### Cas d'Usage Réel : Automation de Code Review

C'est là que HivePilot brille. Une PR arrive :

1. **CodeBot** lit le code, check pour les erreurs de logique, suggère du refactoring
2. **SecurityBot** scanne pour les vulnérabilités, check les patterns auth
3. **PerformanceBot** cherche les N+1 queries, memory leaks, améliorations algorithmiques
4. **DocBot** check si le nouveau code a assez de doc, génère des docstrings
5. **TestBot** vérifie la couverture de tests, suggère les edge cases manquants

Chaque agent tourne en parallèle. Les résultats reviennent en 8-12 secondes (vs 30+ secondes pour de l'analyse séquentielle).

```python
# Usage
hive = HivePilot()
pr_data = fetch_pr_from_github(pr_number)
findings = hive.process_pr(pr_data)

# Output : findings consolidés et conflict-resolved
print(findings)
# {
#   "critical": [...],  # Security issues, logic bugs
#   "moderate": [...],  # Performance, refactoring
#   "minor": [...]      # Documentation, style
# }
```

### Ce Que J'ai Bien Fait

- **Évaluation parallèle** : Différents agents voyant la même chose et arrivant à des conclusions indépendantes catch plus de issues qu'un seul LLM
- **Spécialisation d'agents** : Chaque agent optimisé pour un job veut dire de meilleurs prompts, de meilleurs résultats
- **Partage d'état** : Les agents sachant ce que les autres agents ont trouvé prévient le travail redondant
- **Résilience driven par timeout** : Les agents lents ne blockent pas le pipeline

### Ce Que J'ai Mal Fait

- **Over-orchestration** : Les boucles de résolution de conflits sont chères. Parfois tu as juste besoin d'un agent, pas cinq
- **Efficacité en tokens** : Plus d'agents = plus d'appels LLM. Les économies de l'exécution parallèle ne compensent pas le coût accru
- **Debugger est l'enfer** : Quand un finding est faux, c'est la faute de l'agent? Du partage d'état? De la résolution de conflits? Difficile à tracer

### La Vue d'Ensemble

Les systèmes multi-agents ne sont pas une silver bullet. Ils sont bons quand :
- Les tâches sont naturellement parallèles
- Les agents ont des spécialisations différentes
- Tu peux définir des critères de décision clairs
- Le coût n'est pas la contrainte principale

Ils sont mauvais quand :
- Tu as un budget tight de tokens
- Les tâches sont tightly couplées
- Tu as besoin de la simplicité du single-agent
- Le debugging compte plus que l'accuracy

HivePilot m'a enseigné que l'orchestration est le vrai problème, pas les agents eux-mêmes. N'importe qui peut construire des agents. Construire un système où les agents coordonnent, sont en désaccord gracieusement, et résolvent les conflits — c'est la partie difficile.

C'est pourquoi quand j'ai construit [RTK](/fr/posts/rtk/), ce n'était pas du tout sur les agents — c'était sur éliminer le besoin de l'orchestration complexe en rendant le signal plus propre dès le départ.

### Open Source

[github.com/jsoyer/HivePilot](https://github.com/jsoyer/HivePilot) — c'est rough, c'est pas production-ready, mais les patterns sont là pour quiconque construit des systèmes multi-agents.

Si tu construis des agents, vole la logique de résolution de conflits. Jette la orchestration qui brûle les tokens. Construis quelque chose de plus tight.

---

**Code source** : [github.com/jsoyer/HivePilot](https://github.com/jsoyer/HivePilot) — Apprends de mes erreurs.
