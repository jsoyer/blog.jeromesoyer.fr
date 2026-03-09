---
title: "Zéro papier avec Paperless-ngx : OCR, auto-tags, et fin du chaos documentaire"
date: 2026-03-09T22:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "Gestion de documents auto-hébergée sur Raspberry Pi. OCR, auto-tagging, recherche full-text pour tous vos docs."
categories: ["Homelab", "Automation"]
tags: ["paperless", "homelab", "raspberry-pi", "docker", "automation", "ocr", "self-hosted"]
cover:
  image: /images/covers/paperless-homelab.webp
  alt: "Paperless-ngx homelab setup"
---

J'ai une boîte. Vous en avez probablement une aussi. Elle est remplie de papiers : relevés bancaires, documents d'assurance, déclarations d'impôts, factures d'électricité, contrats — le chaos accumulé de la vie d'adulte. Vous la gardez parce que "j'en aurai peut-être besoin un jour," mais vous ne trouvez jamais vraiment rien dedans. Et quand vous avez besoin de ce document spécifique de 2019 ? Bonne chance pour chercher dans 500 pages de chaos.

Il y a deux ans, j'en ai eu marre. J'ai configuré Paperless-ngx sur mon homelab Raspberry Pi, et maintenant je peux trouver n'importe quel document en 3 secondes en cherchant un mot, une date, ou un nom de correspondant.

## C'est quoi, Paperless-ngx ?

Paperless-ngx est un système open-source de gestion documentaire. Ce n'est pas un outil de stockage cloud (pas de sync vers les serveurs de quelqu'un d'autre), ce n'est pas une app de scanner (bien qu'elle s'intègre avec les scans mobiles), et ce n'est pas un fancy PDF reader. C'est un pipeline documentaire complet : scanner → OCR → tagger → chercher.

Le workflow c'est :

1. Scannez document ou prenez une photo avec le téléphone
2. Déposez dans le dossier "consume" (surveillé par Paperless)
3. Paperless l'OCR (rend les images scannées searchable)
4. Les règles l'auto-taguent basé sur le contenu/expéditeur
5. Parcourez/cherchez depuis l'interface web
6. Les vieux papiers vont à la poubelle de recyclage

Cette dernière étape c'est la vraie magie. Une fois que c'est dans Paperless avec recherche full-text, vous supprimez vraiment le papier physique.

## Setup Docker Compose sur Raspberry Pi

Mon homelab est sur un Raspberry Pi 4 avec 8GB RAM et 1TB SSD USB. Paperless est gourmand en ressources (l'OCR est CPU-lourd), mais c'est gérable.

Voici la config Docker :

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: motdepassesecurise
      POSTGRES_DB: paperless
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7
    volumes:
      - redis_data:/data

  webserver:
    image: ghcr.io/paperless-ngx/paperless-ngx:latest
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"
    environment:
      PAPERLESS_REDIS: redis://redis:6379
      PAPERLESS_DBHOST: postgres
      PAPERLESS_SECRET_KEY: generez_une_vraie_longue_clef_secrete
      PAPERLESS_TIME_ZONE: Europe/Paris
      PAPERLESS_OCR_LANGUAGE: fra,eng
      PAPERLESS_OCR_USER_ARGS: '{"invalidate_upstream_cache": true}'
    volumes:
      - paperless_data:/usr/src/paperless/data
      - paperless_media:/usr/src/paperless/media
      - ./consume:/usr/src/paperless/consume
      - ./export:/usr/src/paperless/export
    restart: unless-stopped

  gotenberg:
    image: gotenberg/gotenberg:latest
    restart: unless-stopped

  tika:
    image: apache/tika:latest
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  paperless_data:
  paperless_media:
```

Le dossier `consume` est où Paperless surveille les nouveaux documents. J'ai un script de scan sur mon iPhone qui upload automatiquement les PDFs ici via un endpoint HTTP simple.

## La magie : règles d'auto-tagging

L'OCR brut est utile, mais l'auto-tagging c'est où le vrai pouvoir vit. Paperless peut créer des règles basées sur le contenu des documents, les patterns de noms de fichier, ou l'information d'expéditeur.

Par exemple :

```python
# Règle 1 : Relevés bancaires
- Name: "Relevés Société Générale"
- Matches: Correspondent "Société Générale"
- Assign: Tag "banque", Document Type "relevé-bancaire"

# Règle 2 : Documents impôts
- Name: "Autorité fiscale française"
- Matches: Content contient "impots.gouv.fr" OU Correspondent "Direction Générale des Finances"
- Assign: Tag "impôts", Document Type "déclaration-impôts"

# Règle 3 : Assurance
- Name: "Documents Assurance"
- Matches: Correspondent contient "assurance" OU Content contient "police"
- Assign: Tag "assurance"

# Règle 4 : Utilitaires
- Name: "Facture EDF"
- Matches: Correspondent "EDF"
- Assign: Tag "utilities", Tag "énergie"
```

Après tagging, chercher est instantané. Besoin de tous vos documents fiscaux 2024 ? Cliquez sur le tag "impôts". Vous cherchez ce sinistre d'assurance spécifique ? Cherchez "sinistre" et obtenez les résultats en millisecondes.

## Le workflow de consommation

J'ai un raccourci sur mon iPhone qui :

1. Ouvre la caméra
2. Prend une photo d'un document
3. L'upload au endpoint consume de Paperless via HTTP POST
4. Affiche une confirmation

Minutes plus tard, le document est OCRé, taguué, et searchable.

Pour les documents physiques sur mon bureau, j'ai un scanner à chargeur feuille Brother ADS-3600W qui peut scanner directement vers un dossier SMB partagé, que j'ai configuré comme symlink vers `consume/`. Déposez une pile de 50 pages, revenez 5 minutes plus tard, et tout est traité.

## Stratégie de backup

Les données Paperless vivent sur le SSD du Pi, qui est redondant (2 disques externes avec RAID), mais je backup aussi vers le cloud en utilisant `restic` :

```bash
#!/usr/bin/env bash
# Backup Paperless vers Backblaze B2
restic backup /home/pi/paperless/data
restic backup /home/pi/paperless/media

# Prune les anciens snapshots (garder 30 derniers jours)
restic forget --keep-last 30 --prune
```

C'est lancé chaque nuit. Si le Pi meurt, je perds au maximum 24 heures de documents (et ils sont probablement déjà dans le dossier consume attendant d'être rescannés de toute façon).

## L'impact réel

La meilleure métrique : j'ai vraiment supprimé des papiers. Des années de relevés et vieux contrats ont été envoyés au recyclage parce que je *savais* qu'ils étaient dans Paperless. C'est la victoire psychologique. La boîte de chaos ? Disparue. Remplacée par une simple base de données searchable.

Trouver des documents est passé de "je m'en occuperai plus tard" à "trouvé en 3 secondes". Ça change le comportement. Je scanne les choses maintenant au lieu de les empiler.

Si vous gérez encore les documents de manière analogique — stocker des boîtes, perdre des reçus, chercher panique pour les contrats — Paperless-ngx est un projet de weekend qui paie des dividendes pendant des années. Self-hosted, open-source, et complètement sous votre contrôle.

Allez scanner du chaos maintenant.
