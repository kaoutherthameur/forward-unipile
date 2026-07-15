---
name: whatsapp-recherche-historique
description: Use when you want to find something someone told you on WhatsApp ("retrouve-moi ce que X m'a dit sur le budget"). Question -> extraits pertinents avec contexte.
---
# Recherche dans l'historique WhatsApp

## Objectif & quand
One-shot : retrouver une information noyée dans vos conversations WhatsApp (un montant, une adresse, une décision, une phrase). Vous posez une question en langage naturel, Claude parcourt l'historique et renvoie les extraits pertinents avec leur contexte (qui, quand, autour de quel échange).

## Prérequis
- Compte(s) WhatsApp (et autres) connecté(s) à Unipile (QR). MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `query` | ce que vous cherchez, en langage naturel (ex : "le budget que Camille a mentionné") |
| `contact_filter` | facultatif : limiter à un contact (nom ou provider_id) pour aller plus vite |
| `limit_chats` | nombre de conversations à balayer |
| `messages_per_chat` | profondeur d'historique par conversation |
| `context_window` | nombre de messages voisins à garder autour de chaque correspondance |
| `output_path` | note markdown de sortie |

## Procédure (via MCP)
1. Lister les conversations WhatsApp (`GET /chats`, filtrées sur le provider WhatsApp), paginer jusqu'à `limit_chats`.
2. Si `contact_filter` est fourni, résoudre le contact via `GET /chat_attendees` et ne garder que sa conversation.
3. Pour chaque conversation retenue, lire l'historique (`GET /chats/{id}/messages`) jusqu'à `messages_per_chat`.
4. Filtrer les messages qui répondent à `query` (mots-clés, synonymes, intention). Pour chaque correspondance, conserver les `context_window` messages avant/après.
5. Classer par pertinence, dater et attribuer chaque extrait (expéditeur via `GET /chat_attendees`).

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
chats = list(u.paginate("chats", params={"provider": "WHATSAPP"}, max_items=50))
msgs = list(u.paginate(f"chats/{chats[0]['id']}/messages", max_items=200))
hits = [m for m in msgs if "budget" in (m.get("text") or "").lower()]
```

## Livrable
Note markdown : un bloc par extrait pertinent (contact, date KR/FR, citation exacte, 1-2 messages de contexte, lien logique avec la question). Une phrase de synthèse en tête si la réponse est claire.

## Limites & anti-ban
Lecture seule (aucune écriture). Compte WhatsApp perso : rester sur de la consultation, pas d'automatisation d'envoi. La recherche est lexicale/sémantique côté Claude, pas un index full-text : sur de très gros historiques, restreindre via `contact_filter`.

## Exemple
`examples/whatsapp-recherche-historique.md` (résultats de recherche fictifs).
