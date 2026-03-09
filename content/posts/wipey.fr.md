---
title: "Wipey : J'ai construit une app macOS parce que je m'envoyais des emails en nettoyant mon clavier"
date: 2026-03-09T21:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "Une app macOS qui verrouille le clavier et le trackpad pendant le nettoyage. Construite en Swift, distribuée via Homebrew."
categories: ["macOS", "Engineering"]
tags: ["swift", "macos", "app", "productivité", "open-source", "engineering"]
cover:
  image: /images/covers/wipey.webp
  alt: "Wipey app macOS verrou clavier"
---

Chaque développeur a connu ça. Vous êtes à votre bureau, le clavier se met à coller à cause du café ou de la poussière, vous attrapez un chiffon microfibre et commencez à nettoyer. Trois secondes plus tard vous avez déclenché trois raccourcis clavier, ouvert Slack, envoyé un message incomplet à un collègue, et basculé sur un buffer Neovim aléatoire. Tout ça parce que vos doigts ont frôlé les touches en essuyant.

Le problème est stupide. La solution était évidente. Donc je l'ai construite.

## Le problème (dont personne ne parle)

Ça paraît ridicule, mais ça arrive à tout le monde :

1. Commencez à nettoyer le clavier avec le chiffon
2. Touchez accidentellement les touches (la mémoire musculaire est bizarre quand les mains sont occupées)
3. Envoyez un email inachevé : "Ouais, je voulais juste vérifi—"
4. Frappez Cmd+W, fermez la mauvaise fenêtre
5. Activez Spotlight d'une manière ou d'une autre et cherchez "jdksl"

J'ai cherché des solutions existantes. Rien ne correspondait. La plupart des apps de verrouillage d'écran sont des outils de sécurité compliqués — trop pour "je ne veux pas accidentellement frapper Cmd+S en essuyant." J'avais besoin de quelque chose de bête simple : verrouiller l'input pendant 30 secondes le temps que je nettoie.

## Wipey : simple par design

Wipey est une petite app macOS dans la barre de menu. Vous configurez un hotkey global (j'utilise Cmd+Shift+L), l'activez, nettoyez votre clavier pendant une minute, et l'input est complètement verrouillé. Pas de clics trackpad, pas de presses clavier, pas de catastrophes accidentelles.

Écrite en Swift avec les API natives, c'est environ 200 lignes de code. Pas de bloat, pas de permissions au-delà du nécessaire, et elle se distribue via Homebrew (pas de taxe App Store, pas de sablonage nonsense).

L'architecture est minimale :

```swift
// Simplifié : écouter le hotkey global
import Cocoa

class InputLock {
    private var eventTap: CFMachPort?

    func lockInput(duration: TimeInterval = 30) {
        eventTap = CGEvent.tapCreate(
            tap: .cghidEventTap,
            place: .headInsertEventTap,
            options: .defaultTap,
            eventsOfInterest: CGEventMask((1 << CGEventType.keyDown.rawValue) |
                                          (1 << CGEventType.mouseMoved.rawValue)),
            callback: { _, _, event, _ in event } // Supprimer tout input
        )

        CFMachPortCreateRunLoopSource(kCFAllocatorDefault, eventTap!, 0)
        DispatchQueue.main.asyncAfter(deadline: .now() + duration) {
            self.unlockInput()
        }
    }

    func unlockInput() {
        CFMachPortInvalidate(eventTap)
        eventTap = nil
    }
}
```

Le vrai travail est fait par `CGEventTap` — une API macOS qui intercepte les événements clavier et souris. Quand Wipey est actif, chaque événement input est supprimé. Quand le timer expiration, le tap est retiré et tout redevient normal.

## Distribution sans les gatekeepers

Wipey est [open-source sur GitHub](https://github.com/jsoyer/Wipey) et disponible via Homebrew :

```bash
brew tap jsoyer/tools
brew install wipey
```

Pas d'App Store, pas de frais annuels, pas de review process. Juste un Homebrew tap qui pointe vers les GitHub releases. Les utilisateurs peuvent inspecter le code, le compiler eux-mêmes s'ils le veulent, ou faire confiance au binaire. Voilà comment les logiciels devraient fonctionner pour les utilitaires.

## Pourquoi c'est important (même si ça semble dumb)

Construire Wipey m'a appris quelque chose qui façonne comment je pense aux outils maintenant :

Les meilleures solutions sont souvent celles qui résolvent *exactement un problème* pour *exactement le bon audience*. Pas tout le monde a besoin d'un verrouilleur de clavier. Mais celui qui maintient un laptop et le nettoie occasionnellement ? Il se sent vu quand tu construis l'outil dont il ne savait pas avoir besoin.

Wipey a accumulé quelques centaines de stars sur GitHub. Les gens l'utilisent. Les gens ouvrent des issues pour ajouter des options de durée, ou un verrouillage par-app (verrouiller seulement quand Notion est actif, par exemple). Chaque feature request est raisonnable parce que le scope est resté tight.

## La leçon meta

J'ai passé peut-être 2 heures à construire Wipey. Le problème qu'il résout prend 5 secondes à expliquer. Ce ratio — "code minimal pour un soulagement maximum" — c'est ce que je chasse maintenant dans tout ce que je construis.

La plupart des logiciels sont sur-engineered. Wipey c'est l'opposé : c'est under-engineered à dessein, et c'est mieux comme ça.

Si vous avez jamais envoyé un email plein de typos à cause de la poussière du clavier, prenez Wipey. Vous vous remercierez.
