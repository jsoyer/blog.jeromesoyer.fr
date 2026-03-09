---
title: "I Built an AI-Powered Job Application Pipeline"
date: 2026-02-19T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "How I over-engineered my job search with a YAML-driven AI pipeline, 67 scripts, and 14 CI/CD workflows. And why I don't regret a second of it."
categories: ["Engineering", "AI"]
tags: ["ai", "automation", "rust", "llm", "productivity", "career", "cli"]
cover:
  image: /images/covers/cv-pipeline.webp
  alt: "AI Job Application Pipeline"
---

I have a confession: I built an entire infrastructure to automate job applications. The technical achievement is worth more than any single outcome it produced.

Here's why I built it, how it works, and what it taught me about recruitment that you probably don't want to know.

### The Problem

You know that feeling when you're applying to jobs and you're manually tweaking your CV for every single position? Removing frameworks that aren't relevant, reorganizing bullet points to highlight the right skills, adding specific keywords from the job description, rewriting your cover letter from scratch each time?

It's exhausting. It's also inefficient. Each CV takes 30 minutes if you're being thorough. And the worst part? You know the hiring system isn't even reading it properly — ATS (Applicant Tracking Systems) are parsing your beautiful formatting and stripping 80% of the signal.

So I did what any engineer would do: I automated the problem away.

### The Architecture

The CV pipeline works in phases:

```
YAML Input → LLM Personalization → Scoring → LaTeX Compilation → PDF Output
```

You start with a YAML spec:

```yaml
target_position: "Senior Software Engineer"
job_description_url: "https://..."
company_culture: "research-driven, AI-focused"
emphasize_skills:
  - "LLVM compilation"
  - "Systems programming"
  - "Distributed systems"
  - "Rust ecosystem"
suppress_skills:
  - "PHP"
  - "legacy systems"
application_style: "direct, technical depth"
```

The pipeline then sends this to 5 LLM providers in parallel:

```bash
# Each provider gets the same spec, the job description, and your base CV
# They each return a personalized CV with different strengths emphasized

./cv-pipeline/bin/personalize \
  --input base-cv.yaml \
  --spec target-role.yaml \
  --providers claude,gpt4,llama,mistral,cohere \
  --output personalized-variants/
```

The system generates 5 distinct variants — each LLM finds different ways to highlight relevance. Claude might reframe your Rust experience as "systems-level thinking". GPT-4 might emphasize your distributed tracing work. Llama might focus on the research angle.

### Scoring and Selection

This is where it gets interesting. The pipeline includes an ATS simulator. It scores each variant against common ATS filters:

```bash
./cv-pipeline/bin/score-ats \
  --cv personalized-variants/*.tex \
  --job-description target-role.txt \
  --output scores.json
```

The scoring system checks for:

- **Keyword matching**: Does the CV include the exact keywords from the job posting?
- **Formatting resilience**: Will the ATS parse this correctly? (Some formatting kills your chances)
- **Section alignment**: Are your most relevant achievements in the first half of the page?
- **Readability**: Enough whitespace that OCR won't choke on it?

Each variant gets a score. The highest-scoring one gets compiled to PDF. You're not relying on the LLM's aesthetics — you're using hard data to pick the winner.

### The Infrastructure

67 shell/Rust/Go scripts. I know because I counted. Some of the key ones:

```bash
# Extract job description from URL
./bin/extract-job-posting.rs \
  --url "https://..." \
  --format yaml \
  --output-dir ./job-specs/

# Compile LaTeX with proper fonts and styling
./bin/tex-compile.go \
  --input personalized.tex \
  --fonts-dir ./assets/fonts/ \
  --output personalized.pdf

# Generate a markdown cover letter tailored to the role
./bin/gen-cover-letter.py \
  --target target-role.yaml \
  --tone technical,direct \
  --output cover-letter.md
```

14 GitHub Actions workflows handle the CI/CD part:

1. **Nightly spec updates** — crawls job boards, adds new specs
2. **Batch personalization** — runs all specs through all providers
3. **Scoring evaluation** — scores all variants
4. **PDF generation** — compiles the winners
5. **Duplicate detection** — makes sure you're not applying twice
6. **Analytics** — tracks which providers perform best for which roles

```yaml
# .github/workflows/nightly-pipeline.yml
name: Nightly Job Application Pipeline
on:
  schedule:
    - cron: "0 2 * * *"
jobs:
  extract:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Extract new job postings
        run: ./bin/extract-job-posting.rs --batch
      - name: Personalize across all providers
        run: ./bin/personalize --parallel --providers claude,gpt4,llama
      - name: Score ATS compliance
        run: ./bin/score-ats --output scores.json
      - name: Compile winners
        run: ./bin/tex-compile --input-dir variants/
      - name: Commit results
        run: git add -A && git commit -m "nightly: $(date +%Y-%m-%d)"
```

### Interview Prep

The pipeline didn't stop at applications. It generates a prep briefing for each interview:

```bash
./bin/gen-interview-prep \
  --company target-company \
  --role "senior-swe" \
  --focus-areas llms,systems,rust \
  --output interview-brief.md
```

This pulls from public sources — company blog posts, engineering talks, GitHub repos, technical papers — and creates a briefing that's actually useful. Not a generic "10 things to know about the company" list. Real technical context.

### What This Taught Me

**On recruitment:**
- The job application process is broken. CVs are a lossy format. ATS systems are approximations. Hiring committees do their best with terrible information.
- Optimization doesn't replace fit. A perfectly tailored CV gets you past the first filter. The rest is execution and luck.
- The signal-to-noise ratio in hiring is worse than in most technical systems. And yet companies still rely on it.

**On AI systems:**
- Multi-LLM orchestration is powerful. Different models have different strengths. Scoring mechanisms are the lever that determines which variant matters.
- Automation works best when you can measure the outcome. ATS scoring is crude but measurable. You can iterate.
- The hardest part isn't the automation — it's defining what "good" looks like when humans won't give you a signal until after you've shipped.

### Open Source

The whole thing is on GitHub: **[github.com/jsoyer/cv-pipeline](https://github.com/jsoyer/cv-pipeline)**

It's not production-ready for other people — the structure is too personal, the specs too idiosyncratic. But the patterns are there: YAML-driven configuration, LLM provider abstraction, scoring systems, LaTeX compilation, CI/CD workflows.

Fork it, build your own. I regret nothing about the time spent. I understand the job search process better, I built something that works, and I learned exactly where applications break down.

Sometimes over-engineering is its own reward.

---

**Source code**: [github.com/jsoyer/cv-pipeline](https://github.com/jsoyer/cv-pipeline) — Fork away.
