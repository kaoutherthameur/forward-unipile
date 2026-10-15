---
name: unipile-prospects-classic
description: Use when you want a prospect list from a free/Classic LinkedIn account (no Sales Navigator). Keywords/filters or a search URL -> CSV of prospects.
---
# Liste de prospects via recherche Classic

## Objectif & quand
One-shot : construire une liste de prospects sans Sales Navigator (compte gratuit/Premium), filtres plus simples.

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic suffit). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `search_url` | (option A) URL d'une recherche LinkedIn classique |
| `filters` | (option B) `keywords`, `network_distance`, `location` |
| `limit` | nombre de profils (max 1000 en Classic) |
| `output_path` | CSV de sortie |

## Procédure (via MCP)
1. `search_url` -> mode URL-based. Sinon `api: "classic"`, `category: "people"`.
2. Lancer `POST /linkedin/search`, paginer via `cursor`.
3. Écrire le CSV.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
res = u.post("linkedin/search", params={"limit": 100},
             json={"api": "classic", "category": "people", "keywords": "head of operations"})
```

## Livrable
CSV : `name, headline, company, location, network_distance, profile_url`.

## Limites & anti-ban
Classic : 1000 résultats max/recherche, ~80-100 profils/jour. Lecture seule.

## Exemple
`examples/prospects-classic.csv` (données fictives, schéma réel).
