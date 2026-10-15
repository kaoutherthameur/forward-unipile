---
name: unipile-commenter
description: Use when you want to comment on a LinkedIn post (or reply to a comment) by API, with optional mentions. Post + text -> comment.
---
# Commenter / répondre sur un post LinkedIn

## Objectif & quand
One-shot : poster un commentaire (ou une réponse à un commentaire) par API. Brique de base d'une auto-réponse aux commentaires de vos posts (variante script ci-dessous).

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `post_url` | URL du post (ou `social_id` URN) |
| `text` | contenu du commentaire (mentions via `{{0}}` + tableau `mentions`) |
| `reply_to_comment_id` | (option) répondre à un commentaire précis |

## Procédure (via MCP)
1. Déduire le `social_id` (URN) du post.
2. Poster (`POST /posts/{social_id}/comments`), avec `comment_id` si réponse.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
sid = u.encode_urn("urn:li:activity:7457342077836767232")
u.post(f"posts/{sid}/comments", json={"text": "Très juste !"}, is_write=True)
```

## Variante récurrente (🔵 script)
Auto-répondre aux commentaires de vos posts : un script qui lit les commentaires récents (`GET /posts/{id}/comments`) et répond (avec garde-fous). Voir `docs/script-template.md`.

## Livrable
Commentaire posté, ou simulé en `DRY_RUN`.

## Limites & anti-ban
Écriture. Reste pertinent et mesuré (le commentaire automatique générique se voit).

## Exemple
Snippet ci-dessus (action one-shot).
