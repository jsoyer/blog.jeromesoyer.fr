---
title: "Intel Mac Renaissance: Building a 128GB Combined RAM Homelab"
date: 2026-03-05T10:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Why I traded my aging Proxmox node for a cluster of high-spec Intel Macs to run Fedora and Windows."
categories: ["Infrastructure", "Hardware", "Linux"]
tags: ["macpro", "macmini", "fedora", "windows", "homelab", "intel"]
---

# [EN] Intel Mac Renaissance: Building a 128GB Combined RAM Homelab

### The 32GB Wall
My previous Homelab center—a custom-built i7 Proxmox node—was a champion for years. But as my development workflow shifted towards local AI, heavy container orchestration, and multi-OS security labs, 32GB of RAM became a suffocating bottleneck. I was constantly fighting swap death and micro-managing service uptimes.

I needed a significant upgrade, but I wanted to stay true to the "Least Privilege Life" philosophy: **maximum control, minimal noise, and efficient hardware reuse.**

### The Strategy: Peak Intel "Sleeper" Macs
Instead of buying a noisy, power-hungry rack server, I looked back at the most iconic and powerful Intel machines Apple ever produced. These machines are currently at the "sweet spot" of the second-hand market: obsolete for macOS power users, but absolute beasts for Linux and Windows servers.

I acquired two specific machines to form my new hybrid cluster:

| Machine | Specs | OS | Role |
| :--- | :--- | :--- | :--- |
| **Mac Pro 2013 (Trashcan)** | Xeon E5 / 64GB RAM | **Fedora Workstation** | Linux Dev & Lab Node |
| **Mac Mini 2018** | Core i7 / 64GB RAM / 1TB | **Windows 11** | High-Perf Windows Node |

Totaling **128GB of RAM** and significant multi-core power, all in a silent, desktop-friendly footprint.

### 🐧 Fedora on the Trashcan: A Masterpiece Reborn
The Mac Pro 2013 is often criticized for its thermal design, but for a headless or dev-focused Linux node, it is incredible. I chose **Fedora Workstation** for this machine. 

Installation was surprisingly smooth. Fedora's kernel handles the Xeon architecture and the dual FirePro GPUs (even if only for basic display) perfectly. With 64GB of RAM, I can now run dozens of Podman containers, local dev environments, and security tools without even hearing the fan spin up. It is the ultimate expression of "Least Privilege": reusing high-quality hardware to run a completely open, local-first OS.

### 🪟 The 64GB Mac Mini: The Ultimate Windows Node
The 2018 Mac Mini was the last of its kind before the T2-equipped Intel transition became "locked down." I found a "maxed out" version with an i7 and **64GB of RAM**. 

I installed **Windows 11** on it to handle my Windows-specific labs and high-performance testing. Most Windows laptops struggle with memory-intensive tasks; this mini-node laughs at them. It’s my dedicated environment for anything that requires the Microsoft ecosystem, isolated from my main dev flow but accessible instantly.

### Lessons Learned
1.  **Hardware is Software-Limited:** These Macs were "too slow" for macOS 15+, but they are incredibly fast for modern Linux and Windows 11.
2.  **Quiet is a Feature:** Having 128GB of RAM running silently next to my desk is a massive improvement over a loud server in a closet.
3.  **Local-First Wins:** By moving away from cloud-hosted instances back to local hardware, I've regained total control over my data and reduced latency to zero.

---

# [FR] Renaissance Intel Mac : Construire un Homelab à 128Go de RAM

### Le mur des 32Go
Mon ancien cœur de Homelab — un nœud Proxmox sous i7 — a été un champion pendant des années. Mais avec l'évolution de mon workflow vers l'IA locale, l'orchestration lourde de containers et les labs de sécurité multi-OS, les 32Go de RAM sont devenus un goulot d'étranglement étouffant. Je passais mon temps à gérer la survie du swap et à micro-manager l'uptime de mes services.

Il me fallait un upgrade sérieux, tout en restant fidèle à la philosophie "Least Privilege Life" : **contrôle maximum, bruit minimum et réutilisation intelligente du hardware.**

### La Stratégie : Les Macs Intel "Sleeper"
Au lieu d'acheter un serveur rack bruyant et énergivore, je me suis tourné vers les machines Intel les plus iconiques et puissantes jamais produites par Apple. Ces machines sont actuellement dans la "zone idéale" du marché de l'occasion : obsolètes pour les utilisateurs macOS, mais de véritables monstres pour des serveurs Linux et Windows.

J'ai acquis deux machines spécifiques pour former mon nouveau cluster hybride :

| Machine | Specs | OS | Rôle |
| :--- | :--- | :--- | :--- |
| **Mac Pro 2013 (Trashcan)** | Xeon E5 / 64Go RAM | **Fedora Workstation** | Nœud Linux Dev & Lab |
| **Mac Mini 2018** | Core i7 / 64Go RAM / 1To | **Windows 11** | Nœud Windows Haute-Perf |

Soit un total de **128Go de RAM** et une puissance multi-cœur massive, le tout dans un format silencieux et compact.

### 🐧 Fedora sur le "Cylindre" : Un Chef-d'œuvre ressuscité
Le Mac Pro 2013 est souvent critiqué pour son design thermique, mais pour un nœud Linux de dev, il est incroyable. J'ai choisi **Fedora Workstation** pour cette machine.

L'installation a été d'une fluidité surprenante. Le kernel de Fedora gère parfaitement l'architecture Xeon. Avec 64Go de RAM, je peux désormais faire tourner des dizaines de containers Podman et mes environnements de dev locaux sans même entendre le ventilateur s'emballer. C'est l'expression ultime du "Moindre Privilège" : réutiliser du hardware de haute qualité pour faire tourner un OS totalement ouvert et local-first.

### 🪟 Le Mac Mini 64Go : Le Monstre Windows
Le Mac Mini 2018 est le dernier de sa lignée avant le verrouillage complet. J'ai trouvé une version "maxée" avec un i7 et **64Go de RAM**.

Je l'ai passé sous **Windows 11** pour gérer mes labs spécifiques à l'écosystème Microsoft et mes tests de haute performance. Là où la plupart des ordinateurs Windows s'essoufflent sur la gestion de la mémoire, ce mini-nœud ne bronche pas. C'est mon environnement dédié pour tout ce qui nécessite Windows, isolé de mon flux de dev principal mais accessible instantanément.

### Leçons apprises
1.  **Le Hardware est limité par le Software :** Ces Macs étaient jugés "trop lents" pour macOS 15+, mais ils sont incroyablement véloces sous Fedora et Windows 11.
2.  **Le Silence est une Feature :** Avoir 128Go de RAM qui tournent silencieusement à côté de mon bureau est une amélioration majeure par rapport à un serveur bruyant dans un placard.
3.  **Le Local-First gagne toujours :** En revenant du cloud vers du hardware local, j'ai repris le contrôle total de mes données et réduit la latence à zéro.

---
*Next up: How I built a modular AI Forge on this new infrastructure.*
*À suivre : Comment j'ai construit une Forge IA modulaire sur cette nouvelle infrastructure.*
