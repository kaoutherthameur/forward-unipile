---
name: unipile-publier-offre
description: Use when you want to create/publish/close a LinkedIn job posting by API from your ATS or tooling. Job fields -> published job.
---
# Publier / gérer une offre d'emploi LinkedIn

## Objectif & quand
One-shot : créer, publier, modifier ou clôturer une offre d'emploi LinkedIn par API (depuis un ATS / un outil interne).

## Prérequis
- Compte LinkedIn **Recruiter** connecté à Unipile. MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `action` | `create` \| `publish` \| `close` |
| `job` | champs de l'offre (titre, entreprise, localisation, description) |
| `job_id` | requis pour `publish` / `close` |

## Procédure (via MCP)
1. `create` -> `POST /linkedin/jobs` (récupère `job_id`).
2. `publish` -> `POST /linkedin/jobs/{job_id}/publish` (gérer un éventuel checkpoint via `POST /linkedin/jobs/checkpoint`).
3. `close` -> `POST /linkedin/jobs/{job_id}/close`.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
res = u.post("linkedin/jobs", json={"title": "...", "location": "...", "description": "..."}, is_write=True)
u.post(f"linkedin/jobs/{res.get('id')}/publish", is_write=True)
```

## Livrable
Offre créée/publiée/clôturée (ou simulée en `DRY_RUN`).

## Limites & anti-ban
Nécessite Recruiter. La publication peut demander une vérification (checkpoint).

## Exemple
Snippet ci-dessus (action one-shot).
