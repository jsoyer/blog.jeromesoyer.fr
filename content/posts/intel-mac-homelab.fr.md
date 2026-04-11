---
title: "Renaissance Intel Mac : Construire un Homelab à 128Go de RAM"
date: 2026-03-05T10:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Pourquoi j'ai remplacé mon nœud Proxmox vieillissant par un cluster de Macs Intel haute performance pour faire tourner Fedora et Windows."
categories: ["Infrastructure", "Hardware", "Linux"]
tags: ["macpro", "macmini", "fedora", "windows", "homelab", "intel"]
cover:
  image: /images/covers/intel-mac-homelab.webp
  alt: "Intel Mac Homelab"
---

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
*Stay local. Stay secure. Live the Least Privilege Life.*
