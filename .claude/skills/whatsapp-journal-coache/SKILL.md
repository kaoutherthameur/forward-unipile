---
name: whatsapp-journal-coache
description: Use when you want to compile a coachee's WhatsApp replies over the week into a progress journal ready for the coaching session, one-shot. chat_id -> point de progression markdown.
---
# Journal de bord d'un coaché (WhatsApp)

## Objectif & quand
One-shot : avant une séance de coaching, compiler toutes les réponses d'un coaché
sur la semaine en un point de progression prêt à l'emploi - répondre à "où en est
Camille cette semaine ?" sans relire manuellement le fil WhatsApp.

## Prérequis
- Compte WhatsApp connecté à Unipile (QR). MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `chat_id` | conversation WhatsApp du coaché |
| `days` | fenêtre à compiler (jours en arrière) |
| `messages_max` | plafond de messages à lire |
| `output_path` | note markdown de sortie |

## Procédure (via MCP)
1. Lire les messages récents du coaché (`GET /chats/{chat_id}/messages`), paginer jusqu'à `messages_max`.
2. Filtrer sur la fenêtre `days` (garder les messages des N derniers jours).
3. Séparer les messages entrants (coaché) des sortants (coach).
4. Synthétiser : actions réalisées, blocages exprimés, questions en attente, points à aborder en séance.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
msgs = list(u.paginate("chats/%s/messages" % "c-3001", max_items=200))
# filtrer par date, séparer entrants/sortants, résumer côté LLM
```

## Livrable
Note markdown : synthèse hebdo (fait / bloqué / en attente) + citations des messages
clés + points à aborder en séance. Voir `examples/whatsapp-journal-coache.md`.

## Limites & anti-ban
Lecture seule (aucun envoi). Compte perso : ne lire que les fils opt-in de coaching.

## Exemple
`examples/whatsapp-journal-coache.md` (données fictives, structure réelle).
