---
title: "Pourquoi j'ai switché sur Nushell (et pourquoi vous devriez peut-être aussi)"
date: 2025-07-23T10:30:00+02:00
draft: false
author: "Jerome Soyer"
description: "Après des années de zsh, j'ai changé mon shell principal pour Nushell. Ce qui a changé, ce qui a cassé, et pourquoi je ne reviens pas en arrière."
categories: ["Tooling", "Terminal"]
tags: ["nushell", "shell", "terminal", "productivity", "cli", "zsh"]
cover:
  image: /images/covers/nushell.webp
  alt: "Why I Switched to Nushell"
---

Il y a un moment dans la vie de tout développeur où on regarde une ligne bash comme ça :

```bash
ps aux | grep "[n]ode" | awk '{print $2}' | xargs kill
```

...et on se dit : *il doit y avoir mieux.*

Il y a. Ça s'appelle **[Nushell](https://www.nushell.sh/)**, et ça traite votre shell comme l'outil de traitement de données qu'il est vraiment.

> **Pour aller plus loin :** Découvrez [Les outils CLI modernes pour 2026](/fr/posts/modern-cli-tools/) — des remplaçants Rust qui se marient parfaitement avec Nushell.

### Le problème avec Bash/Zsh ?

Rien, techniquement. Ça marche. Mais ils ont été conçus à une époque où tout était du texte. Chaque commande sort une chaîne de caractères, et toute votre pipeline est de la manipulation de texte — `awk`, `sed`, `grep`, `cut`. Vous passez la moitié du temps à parser du texte qu'une machine vient de sérialiser pour vous.

### L'idée centrale : tout est données structurées

En Nushell, les commandes retournent des tables, des listes, des enregistrements. Ça change tout :

```nu
# Filtrer une réponse API comme une requête SQL
http get https://api.github.com/repos/nushell/nushell/issues
  | where state == "open"
  | select title created_at user.login
  | sort-by created_at --reverse
  | first 10
```

Pas de `jq`. Pas de `curl | python -m json.tool`. Juste... de la manipulation de données.

### La courbe d'apprentissage

Nushell n'est **pas POSIX**. C'est voulu — et c'est ce qui perturbe le plus au début.

- Pas de `&&` et `||` (utilisez `and`/`or`)
- Pas de `$VAR`, mais `$env.VAR`
- Syntaxe différente pour les scripts et l'interactif

La première semaine est difficile si vous êtes en bash depuis des années. La troisième semaine, vous êtes agacé quand vous devez retourner en bash.

### Verdict

Si vous traitez beaucoup de données en terminal, construisez des pipelines complexes, ou faites de l'admin sys — **le switch vaut le coup**. Les gains de productivité sont réels une fois la courbe passée.

---

*Écrit en faisant tourner Nushell 0.100+ sur macOS et Fedora*
