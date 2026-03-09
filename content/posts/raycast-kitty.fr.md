---
title: "Domptez le Félin : Pilotez Kitty Terminal au doigt et à l'œil avec Raycast"
date: 2026-02-14T10:00:00+01:00
draft: false
tags: ["Raycast", "Kitty", "Terminal", "Productivity", "Automation", "Nushell", "AI"]
categories: ["Tooling"]
author: "Jerome Soyer"
description: "Comment j'ai transformé la gestion de mon terminal en une machine à productivité ronronnante grâce à Raycast et Kitty."
cover:
  image: /images/covers/raycast-kitty.webp
  alt: "Extension Raycast Kitty"
---

Soyons honnêtes deux minutes : on passe 90% de notre vie dans le terminal, et les 10% restants à chercher dans laquelle de nos 57 tabs se cache le `tail -f` qu'on a lancé il y a trois heures.

En tant qu'amoureux inconditionnel de **Kitty** (ce terminal ultra-rapide boosté au GPU) et utilisateur quotidien de **Nushell** (parce que les données structurées, c'est la vie), j'avais besoin d'un pont solide entre mon workflow macOS et mon addiction au CLI.

C'est pour ça que j'ai créé l'extension **Raycast Kitty**. C'est la télécommande que votre terminal attendait.

### 🐱 C'est quoi le programme ?

On n'est pas juste sur un bouton "Ouvrir Kitty" :

*   **Search Kitty Tabs :** Arrêtez de jouer les archéologues. Cherchez parmi tous vos onglets ouverts et sautez sur le bon instantanément.
*   **New Window/Tab :** Parce que bouger la main vers la souris, c'est pratiquement une séance de crossfit non consentie.
*   **Open with Kitty :** Sélectionnez un dossier dans le Finder, lancez la commande, et *paf*—vous y êtes.

### 🚀 La cerise sur le gâteau : Les Launch Configs en YAML

Définissez vos **Configurations de Lancement** en YAML. Imaginez une seule commande qui ouvre Neovim, votre serveur de dev et vos logs dans un layout parfaitement splitté. Le tout lancé en un clic depuis Raycast.

### 🛠 Comment l'installer

L'extension est disponible sur **[GitHub](https://github.com/jsoyer/raycast-kitty)** — installez-la directement via la fonctionnalité "Install Extension from URL" de Raycast, ou clonez et buildez vous-même.

```bash
git clone https://github.com/jsoyer/raycast-kitty
cd raycast-kitty
npm install && npm run build
```

### La suite

La roadmap tourne autour de l'**IA et du "Vibe Coding"** : des fonctionnalités intelligentes qui comprennent le *contexte* de votre tâche en cours et préparent votre environnement Kitty en conséquence. Gestion des layouts en langage naturel. Une extension qui sait que vous êtes en mode "debug incident prod" et ouvre les bons onglets automatiquement.

---

**Code source** : [github.com/jsoyer/raycast-kitty](https://github.com/jsoyer/raycast-kitty)
