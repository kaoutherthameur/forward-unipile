---
name: whatsapp-inbox-unifiee
description: Use when you want one view of all your messaging inboxes (WhatsApp + LinkedIn + Instagram + email) from Claude, one-shot. No input -> inbox groupée par canal + à répondre.
---
# Inbox unifiée multi-canal

## Objectif & quand
One-shot : voir toutes vos messageries au même endroit. Claude lit les conversations de tous les comptes connectés à Unipile (WhatsApp, LinkedIn, Instagram, Messenger, email), les regroupe par canal et signale les non-lues et celles qui attendent une réponse. Répond à "qu'est-ce que j'ai en attente, tous canaux confondus ?".

## Prérequis
- Comptes connectés à Unipile (QR pour WhatsApp/Instagram, OAuth ou QR pour les autres). MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `channels` | canaux à inclure (whatsapp, linkedin, instagram, email...). Vide = tous les comptes connectés |
| `limit_chats` | nombre de conversations à lire par canal |
| `messages_per_chat` | nombre de messages récents par conversation |
| `unread_only` | si vrai, ne garder que les conversations non lues / à répondre |
| `output_path` | note markdown de sortie |

## Procédure (via MCP)
1. Lister les conversations tous providers confondus (`GET /chats` renvoie WhatsApp, LinkedIn, Instagram, email... selon les comptes connectés), paginer jusqu'à `limit_chats` par canal.
2. Si `channels` est renseigné, filtrer sur ces providers.
3. Pour chaque conversation, lire les derniers messages (`GET /chats/{id}/messages`) et les participants (`GET /chat_attendees`).
4. Déterminer le statut : non-lue, à répondre (dernier message entrant), en attente (dernier message sortant).
5. Regrouper par canal, trier par urgence (non-lues d'abord).

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
chats = list(u.paginate("chats", max_items=100))  # tous providers
by_channel = {}
for c in chats:
    by_channel.setdefault(c.get("provider", "?"), []).append(c)
```

## Livrable
Note markdown : une section par canal (WhatsApp, LinkedIn, Instagram, email...), chaque ligne = contact + dernier message + statut (non-lue / à répondre / en attente). Un compteur d'à-répondre par canal en tête.

## Limites & anti-ban
Lecture seule (aucune écriture). Le champ `provider` de chaque chat dépend des comptes réellement connectés : un canal absent de la sortie signifie qu'aucun compte de ce type n'est branché sur Unipile.

## Exemple
`examples/whatsapp-inbox-unifiee.md` (inbox multi-canal fictive).
