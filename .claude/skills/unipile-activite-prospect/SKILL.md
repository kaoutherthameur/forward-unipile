---
name: unipile-activite-prospect
description: Use when preparing to reach out and you want a prospect's recent public activity (their comments and reactions) as conversation hooks. Profile -> activity brief.
---
# Activité publique d'un prospect (accroche)

## Objectif & quand
One-shot : avant un message ou un RDV, récupérer l'activité publique récente d'un prospect (ses commentaires et réactions) pour trouver des angles d'accroche personnalisés.

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `member` | slug ou URL du prospect |
| `limit` | nombre d'items d'activité à récupérer |
| `output_path` | note markdown de sortie |

## Procédure (via MCP)
1. Résoudre le `provider_id` (`GET /users/{identifier}`).
2. Récupérer `GET /users/{id}/comments` et `GET /users/{id}/reactions` (paginer).
3. Synthétiser une note d'accroche (sujets récurrents, posts commentés, tonalité).

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
pid = u.get(f"users/{u.encode_urn(slug)}")["provider_id"]
comments = list(u.paginate(f"users/{u.encode_urn(pid)}/comments", max_items=20))
reactions = list(u.paginate(f"users/{u.encode_urn(pid)}/reactions", max_items=20))
```

## Livrable
Note markdown : sujets récurrents + 2-3 accroches concrètes citant l'activité.

## Limites & anti-ban
Lecture seule. L'activité visible dépend des paramètres de confidentialité du prospect.

## Exemple
`examples/activite-prospect.md` (données fictives, structure réelle).
