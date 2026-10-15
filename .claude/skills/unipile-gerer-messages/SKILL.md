---
name: unipile-gerer-messages
description: Use when you want to act on LinkedIn messages by API - react, edit, delete, or forward a message. Message + action -> done.
---
# Agir sur les messages (réagir / éditer / transférer / supprimer)

## Objectif & quand
One-shot : agir sur un message LinkedIn existant (ajouter une réaction, éditer, supprimer, transférer).

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `message_id` | id du message cible |
| `action` | `react` \| `edit` \| `delete` \| `forward` |
| `value` | emoji (react), nouveau texte (edit), ou `chat_id` cible (forward) |

## Procédure (via MCP)
- `react` -> `POST /messages/{id}/reactions`
- `edit` -> `PUT /messages/{id}`
- `delete` -> `DELETE /messages/{id}`
- `forward` -> `POST /messages/{id}/forward`

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
u.post(f"messages/{mid}/reactions", json={"value": "👍"}, is_write=True)
u.request("PUT", f"messages/{mid}", json={"text": "corrigé"}, is_write=True)
```

## Livrable
Action confirmée (ou simulée en `DRY_RUN`).

## Limites & anti-ban
Écriture. Suppression/édition soumises aux fenêtres LinkedIn.

## Exemple
Snippet ci-dessus (action one-shot).
