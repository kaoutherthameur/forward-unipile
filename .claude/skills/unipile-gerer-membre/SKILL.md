---
name: unipile-gerer-membre
description: Use when you want to follow / unfollow / block a LinkedIn member by API (ad-hoc network management). Member + action -> done.
---
# Suivre / ne plus suivre / bloquer un membre

## Objectif & quand
One-shot : agir sur un membre LinkedIn (suivre, ne plus suivre, bloquer) par API, sans passer par l'interface.

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `member` | slug ou URL du membre |
| `action` | `follow` \| `unfollow` \| `block` |

## Procédure (via MCP)
1. Résoudre le `provider_id` du membre (`GET /users/{identifier}`).
2. Exécuter l'action (`POST /linkedin/members/{id}/action`) avec le type d'action.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
prof = u.get(f"users/{u.encode_urn(slug)}")
u.post(f"linkedin/members/{prof['provider_id']}/action", json={"action": "follow"}, is_write=True)
```

## Livrable
Action confirmée (ou simulée en `DRY_RUN`).

## Limites & anti-ban
Écriture : reste raisonnable en volume. Bloquer est définitif côté LinkedIn.

## Exemple
Voir le snippet ci-dessus (action one-shot, pas de fichier de sortie).
