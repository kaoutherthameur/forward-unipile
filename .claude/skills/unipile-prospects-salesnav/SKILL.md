---
name: unipile-prospects-salesnav
description: Use when you want a qualified prospect list from LinkedIn Sales Navigator (seniority, industry, headcount, changed-jobs filters). Filters or a Sales Nav search URL -> CSV of prospects.
---
# Liste de prospects via Sales Navigator

## Objectif & quand
One-shot : construire une liste ICP ciblée depuis Sales Navigator (filtres avancés) et l'exporter en CSV pour outreach ou import CRM.

## Prérequis
- Compte LinkedIn **Sales Navigator** connecté à Unipile.
- MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `search_url` | (option A) coller l'URL d'une recherche Sales Nav depuis le navigateur |
| `filters` | (option B) filtres structurés (voir exemple) |
| `limit` | nombre de profils à récupérer (max 2500 en Sales Nav) |
| `output_path` | CSV de sortie |

## Procédure (via MCP)
1. Si `search_url` fourni : passer l'URL telle quelle au MCP (mode URL-based).
   Sinon construire les filtres (`api: "sales_navigator"`, `category: "people"`).
2. Récupérer les valeurs d'IDs de filtres si besoin (`GET /linkedin/search/parameters`) - industries, fonctions, séniorités.
3. Lancer la recherche (`POST /linkedin/search`), paginer via `cursor` jusqu'à `limit`.
4. Écrire le CSV.

## Si le MCP ne fait pas l'action
Fallback REST via `lib/unipile_helpers.py` :
```python
from lib import unipile_helpers as u
body = {"api": "sales_navigator", "category": "people",
        "seniority_level": ["Director","VP"], "company_headcount": [{"min":11,"max":200}]}
res = u.post("linkedin/search", params={"limit": 100}, json=body)
```

## Livrable
CSV : `name, headline, company, location, network_distance, profile_url`.

## Limites & anti-ban
Sales Nav : 2500 résultats max/recherche, ~150 profils/jour en récupération. Fractionner par location/industry pour dépasser. La recherche est en lecture (pas d'écriture).

## Exemple
`examples/prospects-salesnav.csv` (données fictives, schéma réel).
