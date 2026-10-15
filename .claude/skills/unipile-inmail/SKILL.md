---
name: unipile-inmail
description: Use when you want to message a LinkedIn member you're NOT connected to (InMail / open profile), one-shot. Recipient + text -> InMail sent.
---
# InMail aux profils hors réseau

## Objectif & quand
One-shot : contacter un membre LinkedIn avec qui tu n'es pas connecté (InMail, ou message gratuit vers un Open Profile).

## Prérequis
- Compte LinkedIn **Sales Navigator** (ou Recruiter) connecté à Unipile. MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `recipient` | slug ou URL du destinataire |
| `subject` | objet de l'InMail |
| `text` | corps du message |
| `linkedin_api` | `sales_navigator` \| `recruiter` |

## Procédure (via MCP)
1. Vérifier le solde de crédits (`GET /linkedin/credits`).
2. Envoyer (`POST /chats` avec `inmail: true`, `recipient_slug`, `linkedin_api`).

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
u.post("chats", json={"inmail": True, "recipient_slug": "camille-lefevre-demo",
                      "linkedin_api": "sales_navigator", "subject": "...", "text": "..."}, is_write=True)
```

## Livrable
InMail envoyé (ou simulé en `DRY_RUN`).

## Limites & anti-ban
Quota mensuel d'InMail selon l'abonnement. Open Profiles : InMail gratuit (max ~800/mois). Impossible de répondre à un InMail non encore accepté.

## Exemple
Snippet ci-dessus (action one-shot).
