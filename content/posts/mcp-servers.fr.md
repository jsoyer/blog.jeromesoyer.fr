---
title: "Serveurs MCP, en pratique : exposer mon homelab à mes agents"
date: 2026-06-24T10:00:00+02:00
draft: false
author: "Jerome Soyer"
description: "Ce qu'est réellement MCP, et la construction pas à pas d'un vrai serveur MCP qui laisse Claude chercher dans mon archive Paperless-ngx — avec les garde-fous de sécurité intégrés."
categories: ["AI", "DevOps", "Automation"]
tags: ["mcp", "ai-agents", "claudecode", "python", "homelab", "automation"]
cover:
  image: /images/covers/mcp-servers.webp
  alt: "Serveurs MCP en pratique"
---

### Le câble manquant entre les agents et tout le reste

Si 2025 a été l'année où les agents sont devenus bons pour écrire du code, 2026 est l'année où ils sont devenus bons pour *faire des choses* — et ce qui a rendu ce saut possible, c'est le **Model Context Protocol**. MCP est, au fond, une idée aussi banale que belle : une manière standard pour un agent IA de découvrir et d'appeler des outils, peu importe qui a construit l'outil ou l'agent.

Avant MCP, chaque intégration était sur mesure. Vous vouliez que Claude interroge votre base de données ? Écrivez un adaptateur de function-calling maison. Vous vouliez la même chose pour Cursor ? Réécrivez-le. MCP fait passer ce problème en N×M à du N+M : les outils parlent MCP, les agents parlent MCP, et ils se trouvent mutuellement.

Je consomme des serveurs MCP depuis des mois — c'est ainsi que mes [dotfiles AI-first](/posts/ai-first-engineering/) atteignent le monde extérieur. Cet article parle d'aller dans l'autre sens : en **construire** un. À la fin, mes agents pourront chercher dans mon [archive documentaire Paperless-ngx](/posts/paperless-homelab/) en langage naturel. Et comme je [viens d'écrire tout un article sur le fait de ne pas confier les clés du royaume aux agents](/posts/securing-ai-agents/), nous le ferons garde-fous activés.

### Le modèle mental

Un serveur MCP expose trois types de choses à un client :

| Primitive | Ce que c'est | Exemple |
|-----------|--------------|---------|
| **Outils (Tools)** | Des fonctions que le modèle peut appeler | `search_documents(query)` |
| **Ressources** | Des données en lecture seule que le modèle peut tirer dans son contexte | `paperless://doc/42` |
| **Prompts** | Des modèles de prompt réutilisables que l'utilisateur peut invoquer | `/summarize-invoice` |

Le client (Claude Code, Claude Desktop, OpenCode, peu importe) lance votre serveur ou s'y connecte, demande « qu'est-ce que tu as ? », et le serveur répond avec un schéma typé pour chaque capacité. À partir de là, le modèle peut appeler vos outils et le client achemine les appels.

Le transport est soit **stdio** (le client lance votre serveur comme sous-processus et communique via stdin/stdout — parfait pour les outils locaux), soit **HTTP/SSE** (pour les serveurs distants). Pour un outil de homelab tournant sur la même machine, stdio est le bon choix : pas de port à exposer, pas de couche d'authentification à rater.

### On construit : un serveur de recherche Paperless

Je vais utiliser le SDK Python officiel avec [`uv`](/posts/mise/) parce qu'il réduit l'histoire des dépendances à une seule ligne. Le serveur entier fait environ 60 lignes.

```bash
uv init paperless-mcp && cd paperless-mcp
uv add "mcp[cli]" httpx
```

Voici `server.py` :

```python
import os
import httpx
from mcp.server.fastmcp import FastMCP

# FastMCP gère pour nous la poignée de main du protocole,
# la génération de schéma et le transport stdio.
mcp = FastMCP("paperless")

PAPERLESS_URL = os.environ["PAPERLESS_URL"]      # ex. http://nas.lan:8000
PAPERLESS_TOKEN = os.environ["PAPERLESS_TOKEN"]  # injecté à la frontière

# Un client en lecture seule. À noter : aucune méthode d'écriture exposée nulle part.
_client = httpx.Client(
    base_url=PAPERLESS_URL,
    headers={"Authorization": f"Token {PAPERLESS_TOKEN}"},
    timeout=10.0,
)


@mcp.tool()
def search_documents(query: str, limit: int = 5) -> list[dict]:
    """Cherche dans l'archive Paperless-ngx en langage naturel.

    Renvoie les documents les plus pertinents avec leur titre, date,
    correspondant et identifiant — jamais le contenu complet.
    """
    limit = max(1, min(limit, 20))  # on borne ; ne jamais faire confiance aux calculs du modèle
    resp = _client.get("/api/documents/", params={"query": query, "page_size": limit})
    resp.raise_for_status()
    return [
        {
            "id": d["id"],
            "title": d["title"],
            "created": d["created"],
            "correspondent": d.get("correspondent"),
            "tags": d.get("tags", []),
        }
        for d in resp.json()["results"]
    ]


@mcp.tool()
def get_document_metadata(document_id: int) -> dict:
    """Récupère les métadonnées d'un document par son ID. Lecture seule."""
    resp = _client.get(f"/api/documents/{document_id}/")
    resp.raise_for_status()
    d = resp.json()
    return {
        "id": d["id"],
        "title": d["title"],
        "created": d["created"],
        "archive_filename": d.get("archive_filename"),
        "tags": d.get("tags", []),
    }


if __name__ == "__main__":
    mcp.run()  # transport stdio par défaut
```

C'est tout le serveur. `FastMCP` introspecte les annotations de type et les docstrings pour générer le schéma JSON que voit le modèle — d'où l'importance des docstrings : **ce sont la documentation de votre outil pour le modèle.** Une docstring vague produit un outil que le modèle utilise mal.

### Le brancher dans Claude Code

Enregistrez le serveur dans votre configuration MCP. Avec Claude Code :

```bash
claude mcp add paperless \
  --env PAPERLESS_URL=http://nas.lan:8000 \
  --env PAPERLESS_TOKEN=op://homelab/paperless/token \
  -- uv run --directory ~/code/paperless-mcp server.py
```

Remarquez le token : je passe une **référence 1Password**, pas le secret lui-même. La valeur est résolue au lancement par `op run` et n'atterrit jamais dans un fichier de configuration, une ligne d'historique shell ou — surtout — quelque part où le modèle peut la lire. C'est le [principe d'hygiène des secrets de l'article sécurité](/posts/securing-ai-agents/) mis en pratique.

Maintenant je peux demander, en langage courant :

> « Trouve ma dernière facture d'électricité et donne-moi la référence du numéro de compte. »

Claude appelle `search_documents("facture électricité")`, récupère les correspondances, choisit la plus récente, appelle `get_document_metadata(...)` et répond. Pas de navigation dans l'interface Paperless, pas besoin de me souvenir des noms de tags.

### Concevoir des outils que le modèle n'utilisera pas de travers

Construire le serveur est facile. Construire un *bon* serveur — que l'agent utilise correctement sous pression — m'a demandé quelques itérations. Ce que j'en ai retiré :

- **Une seule mission par outil.** Un méga-outil avec un paramètre `mode` perturbe le modèle. `search_documents` et `get_document_metadata` valent mieux qu'un unique `documents(action=...)`.
- **Borner et valider tout.** Le modèle passera `limit=10000` s'il pense que ça aide. Ce `max(1, min(limit, 20))` n'est pas de la paranoïa ; c'est la même validation d'entrée que vous écririez pour n'importe quel appelant non fiable — parce que [le modèle *est* un appelant non fiable](/posts/securing-ai-agents/) dès qu'il traite du contenu injecté.
- **Renvoyer le minimum.** Ma recherche renvoie des métadonnées, pas le texte complet du document. Le modèle peut en demander davantage s'il en a besoin. Trop renvoyer gonfle le contexte et élargit la surface d'exposition des données.
- **Rendre les erreurs lisibles.** `raise_for_status()` fait remonter une erreur HTTP propre sur laquelle le modèle peut raisonner, au lieu d'une liste vide silencieuse autour de laquelle il pourrait halluciner.

### Lecture seule par défaut : une fonctionnalité, pas une limite

Vous remarquerez que ce serveur n'a pas de `delete_document`, pas de `update_tags`, aucun chemin d'écriture. C'est délibéré. Les serveurs MCP de homelab les plus utiles que je fais tourner sont des **fenêtres en lecture seule** sur mes systèmes — recherche, statut, métriques, logs. L'agent obtient des yeux, pas des mains.

Quand j'ai *vraiment* besoin d'une capacité d'écriture, elle vit dans un serveur séparé que je n'enregistre que pour la session précise qui en a besoin, et il place les opérations irréversibles derrière une confirmation. Séparer la lecture de l'écriture signifie que mon agent du quotidien — celui qui mâche des issues GitHub non fiables — ne peut physiquement pas muter mon archive, même s'il est entièrement détourné. Il n'avait jamais chargé que le serveur de lecture.

### La suite

Un serveur de recherche, c'est le « hello world » du MCP utile. Le même patron de 60 lignes s'étend à tout ce qui a une API :

- Un serveur **UniFi** qui rapporte quels appareils sont en ligne et signale les nouvelles adresses MAC.
- Un serveur **Grafana** qui tire mes [métriques de sommeil Somneo](/posts/running-data-nerd/) pour que je puisse demander « comment ai-je dormi la semaine dernière ? » sans ouvrir de tableau de bord.
- Un serveur **état du homelab** qui emballe `systemctl`, Podman et l'usage disque dans un unique outil « est-ce que tout va bien ? ».

Chacun transforme une chose que je devais *vérifier* en une chose que je peux *demander*. C'est la vraie promesse de MCP : pas des agents plus tape-à-l'œil, mais des agents enfin branchés sur votre vie réelle — et, si vous le faites bien, branchés avec exactement l'accès dont ils ont besoin, et rien de plus.

Le protocole, c'est la partie facile. La discipline, c'est tout l'enjeu.
