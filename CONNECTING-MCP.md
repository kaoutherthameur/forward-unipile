# Connecter le MCP Unipile (pour les skills 🟢)

Les **skills** de ce repo (`.claude/skills/`) sont pensées pour être lancées **depuis Claude** (Claude Code, Claude Desktop, Cursor...) avec le **serveur MCP Unipile** connecté. Elles couvrent les usages **one-shot / ponctuels** (construire une liste, enrichir un CSV, sortir les engageurs d'un post).

Pour les usages **récurrents / planifiés**, voir les **scripts** (`scripts/`), qui appellent l'API REST directement et se déploient (Modal, cron).

## Setup

Le MCP Unipile est un serveur distant hébergé par Unipile.

`~/.cursor/mcp.json` (ou la config MCP de ton client) — voir `mcp.example.json` :

```json
{
  "mcpServers": {
    "unipile": {
      "url": "https://developer.unipile.com/mcp?branch=v1.0",
      "headers": { "X-API-KEY": "TON_API_KEY" }
    }
  }
}
```

Doc officielle : https://developer.unipile.com/docs/mcp

## Capacité du MCP — matrice & décision d'architecture

> Statut : la doc MCP officielle décrit un serveur qui donne à l'agent un **accès direct à l'API Unipile + la doc + les données temps réel du compte + de l'aide à la génération de code**. La granularité exacte des "tools" exposés (lecture seule vs actions d'écriture) **dépend de la version du serveur MCP** et doit être confirmée dans ton client une fois connecté (liste des tools).

| Famille d'action | Endpoint REST sous-jacent | Attendu via MCP |
|---|---|---|
| Lire comptes / profil | `GET /accounts`, `/users/me`, `/users/{id}` | Oui (lecture) |
| Recherche (people/companies/jobs/posts) | `POST /linkedin/search` | Oui (lecture) |
| Lire posts / réactions / commentaires | `GET /posts/{id}/...` | Oui (lecture) |
| Lire conversations / messages | `GET /chats`, `/messages` | Oui (lecture) |
| Envoyer message / invitation | `POST /chats`, `/users/invite` | **À confirmer** (écriture) |
| Publier post / commenter | `POST /posts`, `/posts/{id}/comments` | **À confirmer** (écriture) |

### Décision (binding des skills)

Chaque `SKILL.md` est écrit pour **piloter le MCP Unipile par intention** (ex : « recherche les profils correspondant à ces filtres », « récupère les commentateurs de ce post »). En tête de chaque skill, une section **« Si le MCP ne fait pas l'action »** renvoie au **fallback REST** : la skill peut alors appeler l'endpoint documenté, ou réutiliser `lib/unipile_helpers.py` exactement comme les scripts.

Conséquence : **les skills marchent que le MCP expose ou non l'écriture.** Les usages en lecture (recherche, enrichissement, engagement) passent par le MCP ; si une action d'écriture n'est pas exposée comme tool, le fallback REST prend le relais. Aucune dépendance bloquante sur la version du serveur MCP.
