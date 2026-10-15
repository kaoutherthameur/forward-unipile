---
name: unipile-inbox
description: Use when you want to read your LinkedIn conversations/messages (multi-account) from Claude, one-shot. No input -> conversations + messages.
---
# Inbox LinkedIn unifiée

## Objectif & quand
One-shot : lire vos conversations LinkedIn (et celles de l'équipe en multi-comptes) depuis Claude - répondre à "qu'est-ce que j'ai reçu ?", "qui attend une réponse ?".

## Prérequis
- Compte(s) LinkedIn connecté(s) à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `limit_chats` | nombre de conversations à lire |
| `messages_per_chat` | nombre de messages récents par conversation |
| `output_path` | note markdown de sortie |

## Procédure (via MCP)
1. Lister les conversations (`GET /chats`), paginer.
2. Pour chaque chat, lire les derniers messages (`GET /chats/{id}/messages`) et les participants (`GET /chat_attendees`).
3. Synthétiser (non-lues, qui attend une réponse).

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
chats = list(u.paginate("chats", max_items=20))
msgs = list(u.paginate(f"chats/{chats[0]['id']}/messages", max_items=10))
```

## Variante récurrente (🔵 script)
Sync continue de l'inbox dans un outil : combiner avec le webhook `webhook_reponses` (F2) pour le temps réel.

## Livrable
Note markdown : conversations + dernier message + statut (à répondre / en attente).

## Limites & anti-ban
Lecture seule.

## Exemple
`examples/inbox.md` (données fictives, structure réelle).
