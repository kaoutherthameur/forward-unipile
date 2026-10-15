---
name: unipile-entreprises-cibles
description: Use when you want a target account list (ABM) from LinkedIn by industry, headcount, location. Filters or a search URL -> CSV of companies.
---
# Liste d'entreprises cibles (ABM)

## Objectif & quand
One-shot : construire une liste de comptes cibles (Account-Based Marketing) filtrée par secteur, effectif, localisation.

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic ou Sales Nav). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `search_url` | (option A) URL d'une recherche d'entreprises |
| `filters` | (option B) `keywords`, `industry`, `headcount`, `location` |
| `limit` | nombre d'entreprises |
| `output_path` | CSV de sortie |

## Procédure (via MCP)
1. `search_url` -> mode URL-based. Sinon `category: "companies"`.
2. Lancer `POST /linkedin/search`, paginer via `cursor`.
3. Écrire le CSV.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
res = u.post("linkedin/search", params={"limit": 100},
             json={"api": "sales_navigator", "category": "companies",
                   "headcount": [{"min": 11, "max": 200}]})
```

## Livrable
CSV : `company, industry, location, followers, jobs_count, company_url`.

## Limites & anti-ban
Sales Nav entreprises : 1000 résultats max. Lecture seule.

## Exemple
`examples/entreprises-cibles.csv` (données fictives, schéma réel).
