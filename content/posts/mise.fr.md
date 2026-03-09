---
title: "mise : un seul outil pour remplacer nvm, rbenv, pyenv et tous les autres"
date: 2026-01-08T10:45:00+01:00
draft: false
author: "Jerome Soyer"
description: "mise consolide tous les gestionnaires de versions de langage dans un seul outil avec config .mise.toml."
categories: ["Tooling", "DevOps"]
tags: ["mise", "cli", "automation", "productivité", "node", "python", "ruby", "go"]
cover:
  image: /images/covers/mise.webp
  alt: "mise gestionnaire de versions runtime"
---

J'ai passé des années noyé dans une mer de gestionnaires de versions. `nvm` pour Node, `rbenv` pour Ruby, `pyenv` pour Python, `gvm` pour Go, et ne me parlez même pas du chaos qui gère vos binaires Rust. Chacun ajoute des hooks shell, chacun est lent au démarrage, et chacun demande son propre rituel de configuration. Ensuite vous sautez entre projets et réalisez que vous tourniez sur Node 16 alors que ce repo a besoin de la 20. Cauchemar.

Bienvenue `mise` — un seul binaire qui remplace *tous les autres*.

## Le problème avec plusieurs gestionnaires de versions

Le problème fondamental n'est pas que ces outils sont mauvais. `nvm` fonctionne bien, `pyenv` est solide. Le problème c'est la fragmentation. Vous vous retrouvez avec :

- Plusieurs hooks d'initialisation shell (démarrage lent)
- Des formats de config différents (certains utilisent `.nvmrc`, d'autres `.python-version`)
- Changement manuel de version par projet
- Pas de moyen unifié de voir ce qui est installé globalement vs localement
- Partager les versions entre projets est un bordel

J'ai vu des équipes perdre des heures sur du "ça marche sur ma machine" parce que quelqu'un avait une version de Node différente sans le savoir.

## mise : un seul outil, tous les runtimes

`mise` est écrit en Rust et fait un seul travail extrêmement bien : gérer les versions de runtime pour n'importe quel langage. C'est via un seul fichier `.mise.toml` par projet (que vous versionnez), et un fichier config global pour les defaults.

L'installation est simple :

```bash
curl https://mise.jdx.dev/install.sh | sh
```

Setup d'un nouveau projet :

```bash
mise use node@22 python@3.12 go@latest
```

Cela crée un `.mise.toml` dans votre projet :

```toml
[tools]
node = "22"
python = "3.12"
go = "latest"
```

Committez ce fichier. Maintenant, n'importe qui clonant le repo exécute `mise` et obtient exactement les mêmes versions automatiquement. Pas de devinettes, pas de cauchemars de version.

## Defaults globaux avec chezmoi

Pour la configuration de ma machine, je garde une config mise globale à `~/.config/mise/config.toml`. Puisque je gère mes dotfiles avec `chezmoi`, je la template pour varier entre mon laptop macOS et ma workstation Fedora Atomic :

```toml
# ~/.config/mise/config.toml (template chezmoi)
[tools]
node = "{{ .node_version }}"
python = "{{ .python_version }}"
rust = "stable"

{{ if eq .chezmoi.os "darwin" }}
# macOS a les outils Xcode
{{ else if eq .chezmoi.osRelease.id "fedora" }}
# Fedora Atomic a une baseline minimale
{{ end }}
```

Le `.chezmoi.toml.tmpl` définit les versions :

```toml
[node_version]
node_version = "22"
python_version = "3.12"
```

Après `chezmoi apply`, mes defaults mise sont cohérents sur les machines.

## Performance : fini le ralentissement shell

`nvm` est célèbre pour ralentir le démarrage du shell parce qu'il s'accroche à chaque nouvelle invocation shell. `mise` c'est différent — c'est un binaire rapide avec un overhead minimal. J'ai mesuré le démarrage du shell qui chute de 50-100ms sur mes machines après migration depuis `nvm`.

`mise` respecte aussi les shims standards (il dépose des exécutables dans `~/.local/share/mise/shims`), donc les outils fonctionnent sans réinitialisation.

## Bonus : task runner

`mise` inclut un lightweight task runner. Au lieu d'un Makefile, vous pouvez définir des tâches dans `.mise.toml` :

```toml
[tasks.test]
run = "npm test"

[tasks.build]
run = "npm run build && cargo build"

[tasks.dev]
run = "npm run dev"
```

Ensuite :

```bash
mise run test
mise run build
```

Pas un remplacement Makefile pour les projets complexes, mais parfait pour des workflows simples.

## Le vrai test

`mise` n'est pas parfait. L'écosystème est encore en maturation — certains runtimes moins courants n'ont pas de plugins. Mais pour Node, Python, Ruby, Go, Rust, et la plupart des langages courants ? C'est rock-solid.

La plus grosse victoire : un fichier config par projet, un config global, un seul outil. Fini le chaos d'initialisation shell, fini les bugs de version, fini le "mais ça marchait en local".

Si vous jonaglez avec plusieurs gestionnaires de versions, essayez `mise` honnêtement. Le soulagement est immédiat.
