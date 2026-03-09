---
title: "J'ai construit un pipeline de candidature alimenté par l'IA"
date: 2026-02-19T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Comment j'ai sur-ingéniérisé ma recherche d'emploi avec un pipeline IA piloté par YAML, 67 scripts et 14 workflows CI/CD. Et pourquoi je ne le regrette pas une seconde."
categories: ["Engineering", "AI"]
tags: ["ai", "automation", "rust", "llm", "productivity", "career", "cli"]
cover:
  image: /images/covers/cv-pipeline.webp
  alt: "AI Job Application Pipeline"
---

J'ai une confession : j'ai construit une infrastructure entière pour automatiser les candidatures d'emploi. L'achievement technique vaut plus que n'importe quel résultat individuel qu'il a produit.

Voici pourquoi je l'ai construit, comment ça marche, et ce que ça m'a appris sur le recrutement que tu ne veux probablement pas savoir.

### Le Problème

Tu connais ce sentiment quand tu postules à des jobs et tu retouches manuellement ton CV pour chaque position? Retirer les frameworks qui ne sont pas pertinents, réorganiser tes bullet points pour mettre en avant les bonnes compétences, ajouter les keywords spécifiques du job posting, réécrire ta lettre de motivation from scratch à chaque fois?

C'est épuisant. C'est aussi inefficace. Chaque CV prend 30 minutes si tu es consciencieux. Et le pire? Tu sais que le système de recrutement ne va pas le lire correctement — les ATS (Applicant Tracking Systems) vont parser ta belle mise en forme et stripper 80% du signal.

Donc j'ai fait ce que tout ingénieur ferait : j'ai automatisé le problème.

### L'Architecture

Le pipeline CV fonctionne en phases :

```
YAML Input → LLM Personalization → Scoring → LaTeX Compilation → PDF Output
```

Tu commences avec une spec YAML :

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

Le pipeline envoie ensuite ça à 5 providers LLM en parallèle :

```bash
# Chaque provider reçoit la même spec, le job description, et ton CV de base
# Ils retournent chacun un CV personnalisé avec des forces différentes

./cv-pipeline/bin/personalize \
  --input base-cv.yaml \
  --spec target-role.yaml \
  --providers claude,gpt4,llama,mistral,cohere \
  --output personalized-variants/
```

Le système génère 5 variantes distinctes — chaque LLM trouve des manières différentes de mettre en avant la pertinence. Claude peut reformuler ton expérience Rust comme "systemic-level thinking". GPT-4 peut mettre l'accent sur ton travail de distributed tracing. Llama peut se concentrer sur l'angle recherche.

### Scoring et Sélection

C'est là que ça devient intéressant. Le pipeline inclut un simulateur ATS. Il score chaque variante contre les filtres ATS courants :

```bash
./cv-pipeline/bin/score-ats \
  --cv personalized-variants/*.tex \
  --job-description target-role.txt \
  --output scores.json
```

Le système de scoring check :

- **Matching des keywords** : Le CV inclut-il les keywords exacts du job posting?
- **Résilience de mise en forme** : L'ATS va-t-il parser ça correctement?
- **Alignement des sections** : Tes achievements les plus pertinents sont-ils dans la première moitié de la page?
- **Lisibilité** : Assez de whitespace pour que l'OCR ne choke pas?

Chaque variante reçoit un score. La meilleure variante est compilée en PDF. Tu ne relies pas sur l'esthétique du LLM — tu utilises des données hard pour choisir le gagnant.

### L'Infrastructure

67 scripts shell/Rust/Go. Je sais parce que j'ai compté. Quelques-uns des clés :

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

14 GitHub Actions workflows gèrent la partie CI/CD :

1. **Nightly spec updates** — crawle les job boards, ajoute des nouvelles specs
2. **Batch personalization** — lance toutes les specs à travers tous les providers
3. **Scoring evaluation** — score toutes les variantes
4. **PDF generation** — compile les gagnants
5. **Duplicate detection** — assure que tu ne postules pas deux fois
6. **Analytics** — track quels providers performent mieux pour quels rôles

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

### Préparation aux Entretiens

Le pipeline ne s'arrêtait pas aux candidatures. Il génère un briefing de préparation pour chaque entretien :

```bash
./bin/gen-interview-prep \
  --company target-company \
  --role "senior-swe" \
  --focus-areas llms,systems,rust \
  --output interview-brief.md
```

Ça pulle des sources publiques — blog de l'entreprise, talks techniques, GitHub repos, papers académiques — et crée un briefing qui est réellement utile. Pas une liste générique "10 choses à savoir sur l'entreprise". Du contexte technique réel.

### Ce Que Ça M'a Appris

**Sur le recrutement :**
- Le processus de candidature est cassé. Les CVs sont un format lossy. Les systèmes ATS sont des approximations. Les hiring committees font de leur mieux avec de l'information terrible.
- L'optimization ne remplace pas le fit. Un CV parfaitement tailored te fait passer le premier filtre. Le reste c'est l'exécution et la chance.
- Le ratio signal-to-noise dans le recrutement est pire que dans la plupart des systèmes techniques. Et pourtant les entreprises y reposent encore.

**Sur les systèmes IA :**
- L'orchestration multi-LLM est puissante. Les modèles différents ont des forces différentes. Les mécanismes de scoring sont le levier qui détermine quelle variante compte.
- L'automation fonctionne mieux quand tu peux mesurer le résultat. L'ATS scoring est crude mais mesurable. Tu peux itérer.
- La partie la plus difficile n'est pas l'automation — c'est de définir ce que "bon" veut dire quand les humains ne vont pas te donner de signal jusqu'après que tu aies shipped.

### Open Source

Le tout est sur GitHub : **[github.com/jsoyer/cv-pipeline](https://github.com/jsoyer/cv-pipeline)**

C'est pas production-ready pour d'autres — la structure est trop personnelle, les specs trop idiosyncrasiques. Mais les patterns sont là : configuration pilotée par YAML, abstraction de provider LLM, systèmes de scoring, compilation LaTeX, workflows CI/CD.

Fork ça, construis le tien. Je regrette rien du temps dépensé. Je comprends mieux le processus de recherche d'emploi, j'ai construit quelque chose qui marche, et j'ai appris exactement où les candidatures se cassent.

Parfois, la sur-ingéniérie est sa propre récompense.

---

**Code source** : [github.com/jsoyer/cv-pipeline](https://github.com/jsoyer/cv-pipeline) — Forke ça.
