---
name: unipile-publier-post
description: Use when you want to publish a LinkedIn post by API (one-shot, or as the building block of a content calendar). Text -> published post.
---
# Publier un post LinkedIn

## Objectif & quand
One-shot : publier un post LinkedIn par API. Brique de base d'un calendrier éditorial (variante script récurrent ci-dessous).

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `text` | contenu du post |
| `visibility` | `PUBLIC` \| `CONNECTIONS` |

## Procédure (via MCP)
1. Composer le `text` (sauts de ligne `\n`).
2. Publier (`POST /posts`).

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
u.post("posts", json={"text": "Mon post...", "visibility": "PUBLIC"}, is_write=True)
```

## Variante récurrente (🔵 script)
Pour un calendrier éditorial : un script cron qui lit une file de posts datés et publie le post du jour (réutilise le même appel + garde-fous). Voir `docs/script-template.md`.

## Livrable
Post publié (id retourné), ou simulé en `DRY_RUN`.

## Limites & anti-ban
Écriture. Évite le sur-posting (1-2/jour max conseillé).

## Exemple
Snippet ci-dessus (action one-shot).
