---
title: "Yapee : J'ai reconstruit un gestionnaire PyLoad parce que Manifest V2 l'a tué"
date: 2026-03-17T10:00:00+01:00
draft: false
author: "Jerome Soyer"
description: "Une extension navigateur moderne pour gérer les téléchargements PyLoad avec chiffrement, mises à jour en temps réel et intégration desktop."
categories: ["Tooling"]
tags: ["browser-extension", "pyload", "téléchargements", "vie-privée", "auto-hébergé"]
cover:
  image: /images/covers/yapee.webp
  alt: "Extension Yapee"
---

Si tu auto-héberges tes téléchargements avec PyLoad, tu as probablement utilisé **Yape** — l'extension navigateur classique qui te permet de gérer tes téléchargements sans ouvrir l'interface web. C'était simple, ça marchait, et puis Google l'a tué. Manifest V2 était deprecated, et Yape était abandonné.

Donc je l'ai reconstruit de zéro. **Yapee** est le successeur spirituel : une extension navigateur moderne pour Chrome, Firefox et Edge qui gère tout ce que l'ancienne extension faisait, plus des features qui rendent la gestion de plusieurs serveurs PyLoad vraiment agréable.

## Pourquoi PyLoad compte toujours

Avant de plonger dans Yapee, parlons de pourquoi PyLoad reste pertinent en 2026. Si tu télécharges des fichiers médias, des eBooks ou des archives, tu connais la douleur : jongler avec plusieurs hébergeurs de fichiers, gérer les quotas, composer avec les captchas. PyLoad est un gestionnaire de téléchargement auto-hébergé qui :

- Gère plusieurs hébergeurs (Rapidgator, Uploaded, Mediafire, 60+ sites)
- Gère l'authentification et les quotas automatiquement
- Résout les captchas avec OCR
- Tourne sur ta propre infrastructure (pas de cloud, pas de tracking)

Ça fonctionne, mais l'interface web est maladroite. Tu veux mettre en file d'attente tes téléchargements sans te logger à chaque fois. C'est là que Yape intervenait — et maintenant Yapee prend sa place.

## Le problème : Manifest V2 est mort

L'ancien Yape fonctionnait bien jusqu'à ce que Google commence à abandonner Manifest V2 en 2024. MV2 permettait des scripts de fond persistants qui pouvaient maintenir des connexions à ton serveur PyLoad indéfiniment. Manifest V3 a tué ce modèle. Les scripts de fond ont une durée de vie limitée, les APIs fetch fonctionnent différemment, et le stockage persistant a changé.

Réécrire pour MV3 n'était pas une tâche mineure — ça signifiait repenser comment l'extension maintient son état, met à jour l'interface, et communique avec PyLoad. L'ancien Yape était abandonné. Donc j'ai commencé de zéro.

## Ce que Yapee fait

Yapee est une extension navigateur qui vit dans ta barre d'outils (Side Panel Chrome sur Chrome, Sidebar sur Firefox). Elle affiche :

- **Les téléchargements actifs** avec des barres de progression, la vitesse et l'ETA
- **L'état de la file d'attente** — pausé, en cours, complété
- **Plusieurs serveurs** — bascule entre tes instances PyLoad en un clic
- **Le mode sombre** avec détection du thème système (respecte ta préférence OS)

Plus important encore, tu n'as pas besoin de mémoriser ton mot de passe PyLoad. Les identifiants sont chiffrés avec **AES-GCM 256-bit** et stockés localement. Pas de serveur, pas de sync cloud, pas de risque de fuite d'identifiants.

### Fonctionnalités clés

**Monitoring en temps réel :** L'extension utilise une architecture event-driven pour rester synchronisée avec ton serveur PyLoad. Quand un téléchargement se termine, tu reçois une notification — l'interface ne fait pas de polling constant.

**Intégration du menu contextuel :** Clique droit sur n'importe quel lien dans ton navigateur, sélectionne "Ajouter à PyLoad", et c'est mis en file. Pas de copier-coller de liens vers l'interface web.

**Collage multi-URL :** Colle 50 liens à la fois. L'extension les parse, filtre les doublons, et les met en file. Utile pour les téléchargements par lot.

**Résolution de captcha dans le popup :** Certains hébergeurs te jettent des captchas. Yapee inclut un popup qui te permet de les résoudre sans quitter ton onglet actuel.

**Support des fichiers conteneurs :** Upload les fichiers conteneurs DLC, CCF ou RSDF directement depuis l'extension.

**Raccourcis clavier :** Ne tends pas la main à la souris. Bascule la sidebar, pause/reprend tes téléchargements, bascule de serveur — tout avec tes propres keybinds.

**Historique de téléchargements :** Vois ce que tu as téléchargé et quand. Utile pour retrouver les fichiers que tu as mis en file il y a des jours.

**i18n :** Anglais et français avec override manuel (bascule de langue sans redémarrer).

**Notifications desktop :** Sois notifié quand les téléchargements se terminent, même si l'extension n'est pas ouverte.

## Le script compagnon Tampermonkey

C'est là que Yapee devient intéressant pour les utilisateurs avancés.

La plupart des sites de téléchargement ont des overlays JavaScript qui hijackent les clics droits ou rendent difficile l'extraction du vrai lien de téléchargement. J'ai écrit un **script Tampermonkey** qui fonctionne aux côtés de Yapee sur 60+ hébergeurs (RapidGator, Uploaded, Mediafire, 1Fichier, Uptobox, etc.).

Le script ajoute un bouton **"Télécharger avec PyLoad"** directement sur la page. Un clic et ton téléchargement est mis en file sans copier-coller. Pour les hébergeurs avec captchas, il remplit les données de captcha et les passe au popup Yapee automatiquement.

C'est le workflow qui rend Yapee utile :

1. Navigue sur un site d'hébergement de fichiers
2. Clique sur "Télécharger avec PyLoad"
3. Résous le captcha si nécessaire (Yapee le gère)
4. Ton serveur PyLoad commence le téléchargement

Pas d'interface web, pas d'extraction manuelle de lien, pas de nonsense clipboard.

## Chiffrement et vie privée

Voici quelque chose à quoi je pense constamment : chaque extension navigateur avec accès à tes identifiants PyLoad est un vecteur de fuite potentiel. La plupart des gestionnaires de téléchargement te demandent de sauvegarder tes identifiants en clair ou de les syncer vers un service cloud.

Yapee ne fait aucun des deux.

Les identifiants sont chiffrés avec AES-GCM en utilisant une clé dérivée de ton mot de passe PyLoad. Même si quelqu'un extrait le stockage de l'extension, il obtient du ciphertext. Le chiffrement se fait localement, et la clé n'est jamais transmise.

Quand tu ajoutes un serveur PyLoad :

1. Tu entres l'URL et le mot de passe
2. Yapee génère une clé AES à partir du mot de passe
3. Les identifiants sont chiffrés et stockés localement
4. Le mot de passe est supprimé de la mémoire
5. Les futures requêtes déchiffrent les identifiants à la volée

Pas de cloud, pas d'authentification tiers, pas de fuites de token.

## Support multi-serveur

Si tu fais tourner plusieurs instances PyLoad (une pour les téléchargements lents, une pour les grabs rapides, une pour les torrents), tu peux les ajouter toutes à Yapee. Un dropdown dans l'extension te permet de basculer de serveur instantanément. Chaque serveur a ses propres identifiants chiffrés.

## État actuel

Yapee en est à la version **3.8.1**. C'est maintenu activement et stable. Je l'utilise quotidiennement sur Chrome et Firefox.

**Ce qui est inclus :**
- Chrome Side Panel (intégration native et moderne)
- Firefox Sidebar (API Sidebar)
- Support Edge (basé sur Chromium)
- Script compagnon Tampermonkey
- Notifications desktop
- Raccourcis clavier
- i18n complet (EN/FR)

**Installation :**

Chrome/Edge : [chrome.google.com/webstore](https://chrome.google.com/webstore) — cherche Yapee

Firefox : [addons.mozilla.org](https://addons.mozilla.org) — cherche Yapee

Script Tampermonkey : [github.com/jsoyer/yapee](https://github.com/jsoyer/yapee)

## Pourquoi c'est important

Reconstruire Yapee m'a appris quelque chose d'important sur les extensions : elles sont de plus en plus la colle entre le web et ton infrastructure personnelle. La plupart des extensions sont soit abandonnées soit en train de se transformer en vecteurs de tracking.

Yapee respecte ta vie privée parce qu'elle est auto-hébergée. Ton serveur PyLoad tourne sur tes propres machines. Tes identifiants ne quittent jamais ta machine. L'extension est juste une couche UI qui parle directement à *ton* infrastructure.

Si tu utilises toujours PyLoad, essaie Yapee. Ça enlève la friction de la gestion des téléchargements entre plusieurs hébergeurs et serveurs.

## Crédits

Yapee se dresse sur les épaules de **Yape** par Rémi Rigal. Je suis reconnaissant envers l'outil original qui a prouvé le concept. Quand Google a tué Manifest V2, quelqu'un devait le reconstruire pour le web moderne. Ce quelqu'un s'est avéré être moi.

---

**Code source :** [github.com/jsoyer/yapee](https://github.com/jsoyer/yapee)

**Signale les problèmes :** [github.com/jsoyer/yapee/issues](https://github.com/jsoyer/yapee/issues)
