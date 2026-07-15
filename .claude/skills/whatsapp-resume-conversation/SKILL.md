---
name: whatsapp-resume-conversation
description: Use when a WhatsApp client thread is long and you need a summary. Fil de conversation -> récap + prochaine action recommandée.
---
# Résumer un fil WhatsApp client

## Objectif & quand
One-shot : condenser un fil WhatsApp client long (SAV, commande, réservation) en un récap clair + la prochaine action recommandée, pour reprendre le dossier sans tout relire.

## Prérequis
- Compte WhatsApp connecté à Unipile (QR). MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `chat_id` | id du fil WhatsApp à résumer |
| `messages_a_lire` | nombre de messages récents à récupérer |
| `output_path` | note markdown de sortie |

## Procédure (via MCP)
1. Lire les messages du fil (`GET /chats/{chat_id}/messages`), paginer jusqu'à `messages_a_lire`.
2. Récupérer les participants si utile (`GET /chats/{chat_id}` ou `chat_attendees`) pour distinguer client et vous.
3. Synthétiser : contexte, demande initiale, points clés, engagements pris, statut actuel.
4. Déduire la prochaine action recommandée (répondre, escalader, clôturer).

## Si le MCP ne fait pas l'action
Fallback REST via `lib/unipile_helpers.py` :
```python
from lib import unipile_helpers as u
msgs = list(u.paginate(f"chats/{chat_id}/messages", max_items=50))
```
Endpoint sous-jacent : `GET /chats/{id}/messages`.

## Livrable
Note markdown : titre du dossier, résumé (3-5 puces), engagements en cours, statut, **prochaine action recommandée**.

## Limites & anti-ban
Lecture seule (aucun envoi). Rien à surveiller côté ban.

## Exemple
`examples/whatsapp-resume-conversation.md`.
