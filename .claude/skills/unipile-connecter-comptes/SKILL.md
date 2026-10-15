---
name: unipile-connecter-comptes
description: Use when you set up Unipile - connect a LinkedIn account (hosted auth or cookie), handle checkpoints (2FA/captcha), and manage your team's connected accounts.
---
# Connecter & gérer les comptes LinkedIn (setup)

## Objectif & quand
Setup / one-shot : connecter un (ou plusieurs) compte(s) LinkedIn à Unipile et les piloter. Couvre le socle de démarrage (S1) : auth + gestion des checkpoints.

## Prérequis
- Clé API Unipile (`UNIPILE_API_KEY`, `UNIPILE_DSN`). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `method` | `hosted` (assistant Unipile) \| `cookie` (token `li_at`) |

## Procédure (via MCP)
1. **Hosted Auth** (recommandé) : `POST /hosted/accounts` → renvoie une URL où l'utilisateur se connecte. Le moins de code.
2. **Cookie** : `POST /accounts` avec le `li_at` + user agent (plus stable face aux checkpoints).
3. **Checkpoints** (2FA, captcha, validation app) : `POST /accounts/checkpoint` (et `.../checkpoint/resend`). 5 min pour résoudre.
4. **Gérer** : `GET /accounts` (lister/statut), `POST /accounts/{id}/reconnect`, `PATCH /accounts/{id}/proxy`.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
print(u.get("accounts"))            # comptes connectés + statut
```

## Livrable
Compte(s) connecté(s) et listés, prêts pour les autres skills/scripts.

## Limites & anti-ban
Un compte par profil LinkedIn. Configurer un proxy stable par compte pour réduire les checkpoints. Multi-comptes = répartition de la charge (anti-ban).

## Exemple
`GET /accounts` (snippet ci-dessus).
