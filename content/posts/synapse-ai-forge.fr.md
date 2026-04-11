---
title: "Synapse : Construire une Forge IA Modulaire sous Fedora 43"
date: 2026-03-25T11:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Une plongée dans le provisionnement automatisé d'un nœud IA haute performance avec RTX 5070 et Podman rootless."
categories: ["AI", "DevOps", "Fedora"]
tags: ["rtx5070", "podman", "ollama", "uv", "automation", "nvidia", "fedora"]
cover:
  image: /images/covers/synapse-ai-forge.webp
  alt: "Synapse AI Forge"
---

### Au-delà du Chatbot
Si vous suivez ce blog, vous connaissez mon obsession pour les systèmes local-first. Faire tourner un LLM de base est facile. Construire une **infrastructure IA de niveau professionnel**, reproductible, sécurisée et performante, est une autre histoire.

Voici **Synapse** : ma forge IA dédiée. Alors que mes Macs gèrent les interfaces, Synapse s'occupe du travail lourd. Basé sur **Fedora 43**, il est conçu pour offrir un environnement "zero-trust" pour l'entraînement et l'inférence.

### La Stack Hardware
Pour gérer des modèles modernes (Llama 3, Mistral) avec de grands contextes, j'ai choisi un équilibre entre nombre de cœurs et VRAM :
*   **CPU :** AMD Ryzen 7 3700X (8c/16t)
*   **GPU :** NVIDIA RTX 5070 (**12Go VRAM**, architecture Blackwell)
*   **RAM :** 32Go DDR4
*   **Stockage :** 1To NVMe SSD

La RTX 5070 est la star ici. Son architecture Blackwell permet une inférence et une quantification incroyablement rapides, ce qui en fait le cœur parfait pour une forge locale.

### Provisionnement Modulaire : L'Architecture 00-10
Je n'installe plus rien manuellement. J'ai développé un système de provisionnement modulaire composé de 11 scripts (numérotés de 00 à 10) qui transforment une Fedora fraîche en un lab IA opérationnel en quelques minutes.

#### 1. Système & GPU (Scripts 00-03)
Cette couche gère le "sale boulot" : mise à jour des paquets, configuration de `firewalld` et installation de la stack de drivers NVIDIA. Élément crucial : la mise en place du **Container Device Interface (CDI)**, qui permet à Podman d'accéder au GPU sans la complexité des runtimes Docker traditionnels.

#### 2. Le Moteur Python : `uv` (Scripts 04-05)
J'ai complètement remplacé `pip` et `conda` par **[`uv`](https://github.com/astral-sh/uv)**. Il gère mes environnements **Python 3.12** avec une vitesse quasi instantanée. Chaque tâche IA (Training, RAG, Serving) a son propre environnement isolé, évitant ainsi l'enfer des dépendances.

#### 3. Services Rootless (Scripts 06-08)
La sécurité est primordiale. Chaque service IA tourne en **mode Podman rootless** via `podman-compose` :
*   **Ollama & vLLM :** Moteurs d'inférence haute performance.
*   **Qdrant :** Ma base de données vectorielle pour le stockage de la connaissance locale.
*   **Open-WebUI :** L'interface pour interagir avec mes modèles.
*   **Redis & Postgres :** Pour le cache et la gestion d'état.

#### 4. Observabilité & Modes de Forge (Scripts 09-10)
J'ai implémenté un utilitaire **"Forge Mode"**. Avec 12Go de VRAM, je ne peux pas tout faire tourner en même temps. Cet outil me permet de basculer entre des profils :
*   **`forge-mode chat`** : Lance Ollama et l'interface Web.
*   **`forge-mode training`** : Coupe l'interface pour libérer chaque Mo de VRAM pour **Unsloth** et le fine-tuning.

### Pourquoi Fedora 43 ?
Fedora reste le meilleur terrain de jeu pour l'IA car elle propose les derniers kernels et drivers. Elle supporte Podman rootless et la stack NVIDIA mieux que presque n'importe quelle autre distribution, s'inscrivant parfaitement dans la philosophie "Least Privilege" : **moderne, sécurisée et rapide.**

---
*Stay local. Stay secure. Live the Least Privilege Life.*
