---
name: unipile-sourcing-candidats
description: Use when you open a role and want a candidate shortlist from LinkedIn (Recruiter or Sales Navigator) filtered by skills, seniority, industry. Filters -> CSV shortlist.
---
# Sourcer des candidats LinkedIn

## Objectif & quand
One-shot : à l'ouverture d'un poste, construire une shortlist de candidats filtrée (compétences, séniorité, secteur) exportée en CSV.

## Prérequis
- Compte LinkedIn **Recruiter** ou **Sales Navigator** connecté à Unipile.
- MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `search_url` | (option A) URL d'une recherche Recruiter/Sales Nav |
| `filters` | (option B) filtres structurés (rôle, skills, séniorité) |
| `limit` | nombre de candidats (max 2500) |
| `output_path` | CSV de sortie |

## Procédure (via MCP)
1. `search_url` fourni -> mode URL-based. Sinon construire les filtres avec `api: "recruiter"` (ou `"sales_navigator"`), `category: "people"`.
2. Au besoin, résoudre les IDs (`GET /linkedin/search/parameters`) pour `skills`, `function`, `industry`.
3. Lancer (`POST /linkedin/search`), paginer via `cursor` jusqu'à `limit`.
4. Écrire le CSV.

## Si le MCP ne fait pas l'action
Fallback REST via `lib/unipile_helpers.py` :
```python
from lib import unipile_helpers as u
body = {"api": "recruiter", "category": "people",
        "role": {"keywords": "data engineer", "priority": "MUST_HAVE", "scope": "CURRENT_OR_PAST"}}
res = u.post("linkedin/search", params={"limit": 100}, json=body)
```

## Livrable
CSV : `name, headline, current_title, location, network_distance, profile_url`.

## Limites & anti-ban
Recruiter : 2000 profils/jour, 2500 résultats/recherche. Lecture seule. L'approche candidats (invitation/InMail) est un autre cas d'usage (voir scripts d'outreach).

## Exemple
`examples/sourcing-candidats.csv` (données fictives, schéma réel).
