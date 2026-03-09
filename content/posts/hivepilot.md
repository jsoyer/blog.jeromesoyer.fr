---
title: "HivePilot: Building a Multi-Agent AI Orchestration System From Scratch"
date: 2026-02-05T09:30:00+01:00
draft: true
author: "Jerome Soyer"
description: "How I built a multi-agent orchestration system in 2024 when the tools barely existed. What worked, what exploded, and why agent swarms are harder than you think."
categories: ["Engineering", "AI"]
tags: ["ai", "automation", "llm", "agents", "productivity", "python", "engineering"]
cover:
  image: /images/covers/hivepilot.webp
  alt: "HivePilot Multi-Agent System"
---

The moment you realize that a single LLM isn't enough, you're building multi-agent systems. You don't choose to — you just end up there.

I built **[HivePilot](https://github.com/jsoyer/HivePilot)** in late 2024, when multi-agent frameworks were mostly theoretical. The problem was simple: some tasks are too complex for one model to nail, but perfect for a swarm of specialized agents. Code review automation, documentation generation, integration testing — these need different angles.

Here's what I learned about orchestrating agents, why it's harder than it looks, and where the whole thing nearly fell apart.

### The Problem Single Agents Can't Solve

Imagine this: You want an AI system to automatically review your pull requests, flag issues, suggest improvements, and generate documentation for new files.

A single LLM can do it. It'll read the PR, check the logic, make suggestions. But it'll miss things:
- Edge cases that need domain-specific knowledge
- Security issues that require threat modeling
- Performance regressions that need benchmarking context
- Documentation that needs both technical accuracy and readability

You *could* prompt engineer your way around this. Add 40 more instructions, context, examples, feedback loops.

Or you could do what I did: build a hive.

### HivePilot Architecture

The core concept is simple: **agents are workers, an orchestrator is the boss**.

```
┌─────────────────────────────────┐
│     Central Orchestrator         │
│  (Manages state, routing, flow)  │
└────────┬────────────┬────────────┘
         │            │
    ┌────▼──┐    ┌────▼──┐
    │CodeBot│    │DocBot  │     Each agent is
    │       │    │        │     specialized for
    └───────┘    └────────┘     one job
    ┌──────┐    ┌────────┐
    │SecBot│    │TestBot │
    │      │    │        │
    └──────┘    └────────┘
```

The orchestrator works like this:

```python
# Simplified HivePilot orchestrator logic
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
        # Phase 1: Parse the PR
        self.state.pr = parse_pr(pr_data)

        # Phase 2: Dispatch to agents in parallel
        results = {}
        for agent_name, agent in self.agents.items():
            results[agent_name] = agent.analyze(
                self.state.pr,
                context=self.state.context
            )

        # Phase 3: Aggregate findings
        return self.aggregate_findings(results)
```

Each agent operates independently but shares state. The orchestrator routes work, manages dependencies, and aggregates findings.

### The Challenges That Nearly Broke Me

**1. State Management is Insane**

The first problem: agents need to see the same code but reach different conclusions. If the CodeBot analyzes a function and marks it as "needs refactoring", the SecurityBot needs to know that so it doesn't spend time on already-flagged code.

But agents also need independence. If one agent crashes, others keep working.

```python
# The solution: immutable state snapshots
@dataclass
class HiveState:
    pr_data: Dict  # Original PR (immutable)
    context: Dict  # Shared context
    findings: Dict[str, List[Finding]]  # Per-agent findings

    def get_snapshot_for_agent(self, agent_name):
        """Each agent gets a read-only copy of current state"""
        return HiveStateSnapshot(
            pr_data=deepcopy(self.pr_data),
            context=deepcopy(self.context),
            previous_findings=self.findings  # Read-only
        )
```

**2. Agents Arguing With Each Other**

This happened. SecurityBot flags a pattern as a vulnerability. CodeBot reviews the same code and says "nope, that's fine, it's a common pattern."

They both call the orchestrator with conflicting findings. Now what?

I added a "conflict resolution" phase:

```python
def resolve_conflicts(self, findings_dict):
    """When agents disagree, ask them to justify"""
    conflicts = self.detect_conflicts(findings_dict)

    for conflict in conflicts:
        # Re-run both agents with explicit conflict awareness
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

        # Accept whichever has stronger confidence + evidence
        return self.pick_stronger_finding(agent1_result, agent2_result)
```

It's not perfect but it reduces hallucinations.

**3. Infinite Loops**

An agent submits a finding. The orchestrator routes it to another agent for verification. That agent submits a follow-up question. First agent responds. Second agent questions the response.

Before you know it, you've got 47 agent-to-agent messages and you're burning tokens like it's a LLM API free tier.

```python
# Solution: max depth + decision timeout
class AgentMessage:
    content: str
    depth: int  # Track conversation depth
    timestamp: float

def route_message(self, message, max_depth=3):
    if message.depth >= max_depth:
        # Force resolution: escalate to orchestrator
        return self.orchestrator_decides(message)

    # Also timeout: if message chain takes > 30 seconds, force resolution
    if time.time() - message.timestamp > 30:
        return self.orchestrator_decides(message)

    return self.route_to_next_agent(message)
```

**4. One Agent Crashes, Everything Slows Down**

If CodeBot takes 45 seconds to respond and others finish in 2 seconds, you're waiting 45 seconds for the complete result.

I added agent timeouts and fallback strategies:

```python
async def wait_for_agents(self, agent_tasks, timeout=10):
    """Gather results with timeouts"""
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
                # Agent timed out — use fallback
                results[agent_name] = self.fallback_analysis(agent_name)

    except Exception as e:
        results["error"] = str(e)

    return results
```

### Real Use Case: Code Review Automation

This is where HivePilot shines. A PR comes in:

1. **CodeBot** reads the code, checks for logic errors, suggests refactoring
2. **SecurityBot** scans for vulnerabilities, checks authentication/authorization patterns
3. **PerformanceBot** looks for N+1 queries, memory leaks, algorithmic improvements
4. **DocBot** checks if new code has adequate documentation, generates docstrings
5. **TestBot** verifies test coverage, suggests missing edge cases

Each agent runs in parallel. Results come back in 8-12 seconds (vs 30+ seconds for sequential analysis).

```python
# Usage
hive = HivePilot()
pr_data = fetch_pr_from_github(pr_number)
findings = hive.process_pr(pr_data)

# Output: consolidated, conflict-resolved findings
print(findings)
# {
#   "critical": [...],  # Security issues, logic bugs
#   "moderate": [...],  # Performance, refactoring
#   "minor": [...]      # Documentation, style
# }
```

### What I Got Right

- **Parallel evaluation**: Different agents seeing the same thing and reaching independent conclusions catches more issues than a single LLM
- **Agent specialization**: Each agent optimized for one job means better prompts, better results
- **State sharing**: Agents knowing what other agents found prevents redundant work
- **Timeout-driven resilience**: Slow agents don't block the pipeline

### What I Got Wrong

- **Over-orchestration**: Conflict resolution loops are expensive. Sometimes you just need one agent, not five
- **Token efficiency**: More agents = more LLM calls. The savings from parallel execution don't offset the increased cost (I should have built in token budgets)
- **Debugging is hell**: When a finding is wrong, is it the agent's fault? The state sharing? The conflict resolution? Hard to trace

### The Bigger Picture

Multi-agent systems are not a silver bullet. They're great when:
- Tasks are naturally parallel
- Agents have different specializations
- You can define clear decision criteria
- Cost isn't the primary constraint

They're terrible when:
- You're on a tight token budget
- Tasks are tightly coupled
- You need single-agent simplicity
- Debugging matters more than accuracy

HivePilot taught me that orchestration is the real problem, not the agents themselves. Anyone can build agents. Building a system where agents coordinate, disagree gracefully, and resolve conflicts is the hard part.

That's why when I built [RTK](/posts/rtk/), it wasn't about agents at all — it was about eliminating the need for complex orchestration by making the signal cleaner upfront.

### Open Source

[github.com/jsoyer/HivePilot](https://github.com/jsoyer/HivePilot) — it's rough, it's not production-ready, but the patterns are there for anyone building multi-agent systems.

If you're building agents, steal the conflict resolution logic. Throw away the token-burning orchestration. Build something tighter.

---

**Source code**: [github.com/jsoyer/HivePilot](https://github.com/jsoyer/HivePilot) — Learn from my mistakes.
