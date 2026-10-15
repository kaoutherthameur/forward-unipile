---
name: unipile-audit-followers
description: Use when you want to list and compare your LinkedIn followers and the accounts you follow. No input -> CSV of followers + following.
---
# Auditer followers & following

## Objectif & quand
One-shot : lister vos abonnés et les comptes que vous suivez (audit, repérer les non-réciproques).

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `output_path` | CSV de sortie |

## Procédure (via MCP)
1. `GET /users/followers` (paginer) et `GET /users/following` (paginer).
2. Marquer chaque personne : `is_follower`, `is_following`.
3. Écrire le CSV.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
followers = list(u.paginate("users/followers"))
following = list(u.paginate("users/following"))
```

## Livrable
CSV : `name, headline, profile_url, is_follower, is_following`.

## Limites & anti-ban
Lecture seule.

## Exemple
`examples/audit-followers.csv` (données fictives, schéma réel).
