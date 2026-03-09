---
title: "Ma cave numérique : comment j'ai mis ma collection de vins dans une base de données"
date: 2026-03-09T11:00:00+01:00
draft: true
author: "Jerome Soyer"
description: "Quand votre cave devient un chaos, il est temps de lui appliquer une bonne dose d'organisation geek et d'automatisation."
categories: ["Life", "Homelab"]
tags: ["vin", "homelab", "automation", "self-hosted", "data", "vie"]
cover:
  image: /images/covers/cave-numerique.webp
  alt: "Cave à vin numérique"
---

Il y a un an, j'ai réalisé que je n'avais aucune idée de ce qui était réellement dans ma cave à vin. Oh, je savais qu'il y avait des bouteilles — beaucoup de bouteilles — mais où était ce Bordeaux 2018 que j'avais acheté ? Est-ce que j'avais déjà bu ce Bourgogne ? Combien de Côtes du Rhône ai-je ? C'était le chaos.

Pendant une semaine, j'ai considéré faire une simple liste Excel. Puis je me suis dit, "non, ça ne suffira pas." Je suis un data nerd. C'est mon élément.

J'ai commencé par identifier ce que je voulais tracker : millésime, appellation, domaine, région, position exacte dans la cave (parce que oui, j'ai numéroté les emplacements), notes de dégustation personnelles, prix payé, date d'acquisition, apogée estimée. Vous voyez le truc. Trop, probablement. Parfait.

J'aurais pu utiliser une base de données existante comme Cellarestm ou Vivino, mais où serait le plaisir ? J'ai construit quelque chose sur SQLite avec une petite interface web custom. Rien de compliqué — une application simple en Python avec Flask, une base de données locale, et quelques requêtes SQL pour exploiter les données.

Le truc vraiment amusant est venu avec l'automatisation. J'avais environ 80 bouteilles à entrer manuellement. Douleur. Alors j'ai hacké quelque chose : un script qui scanne les étiquettes des bouteilles via ma caméra de téléphone, utilise une OCR basique pour extraire les informations clés (domaine, millésime, appellation), puis j'affine manuellement les détails. C'est inspiré de Paperless-ngx, mais appliqué au vin. Ça m'a économisé des heures de saisie manuelle.

Maintenant quand j'achète une bouteille, j'ai une petite routine : je la scan, les infos principales sont pré-remplies, j'ajoute mes notes si c'est une bouteille que j'ai déjà essayée, et elle est cataloguée. C'est devenu satisfaisant, même un peu méditative dans sa façon geeky.

Mais c'est surtout utile. Je peux maintenant interroger ma cave : "Quels vins ai-je qui sont à l'apogée maintenant ?" Ma base de données me le dit. "Quel Bourgogne non-ouvert reste-t-il ?" Une requête. "Montrez-moi les vins avec un rapport qualité-prix de plus de 8/10." Voilà. Je peux même faire des statistiques sur mes achats — quelles régions j'achète le plus, quelle gamme de prix je préfère.

Et pour les mariages mets-vins ? Au lieu de galérer à chercher ma mémoire, je filtre par profil gustatif stocké. Riche et tannique ? Léger et fruité ? Voilà ce que j'ai.

Évidemment, c'est probablement excessif pour une cave de 80-100 bouteilles. La plupart des gens appelleraient ça "trop," et ils auraient raison. Mais c'est aussi fun, et c'est devenu l'une de ces petites victoires du homelab où vous construisez un truc juste parce que vous pouvez. C'est devenu un vrai outil, pas juste un exercice de programmation.

L'ironie ? Maintenant que je sais exactement ce que j'ai, j'achète moins. C'est plus difficile de justifier l'achat impulsif quand la base de données me montre que j'ai déjà quatre Côtes du Rhône de ce domaine. C'est peut-être le vrai bénéfice — une cave bien organisée, c'est une cave mieux gérée.

Si vous êtes aussi obsédé que moi, pensez à tracker votre cave. Vous ne regretterez pas l'investissement en temps. Et qui sait, vous ferez peut-être quelques découvertes agréables en explorant vos propres données.
