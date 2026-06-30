---
name: unipile-raw-voyager
description: Use when a LinkedIn data point isn't exposed by a standard Unipile endpoint and you need to proxy an internal Voyager endpoint (advanced). Voyager URL -> raw JSON.
---
# Raw proxy Voyager (avancé)

## Objectif & quand
One-shot avancé : accéder à un endpoint interne LinkedIn (Voyager) non standardisé par Unipile, via le proxy `getRawData`. Exemple éprouvé : "qui a vu mon profil" (`wvmpCards`, voir le script `profile_views`).

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `request_url` | URL de l'endpoint Voyager à proxifier |
| `method` | méthode HTTP (souvent `GET`) |

## Procédure (via MCP / REST)
`POST /linkedin` (getRawData) avec `{ account_id, request_url, method, headers }`.
Le helper existe déjà :
```python
from lib import unipile_helpers as u
data = u.raw_voyager("https://www.linkedin.com/voyager/api/identity/wvmpCards")
```

## Livrable
JSON Voyager brut (structure en "union dicts" `{fqcn: value}` à parser).

## Limites & anti-ban
Avancé : structure fragile aux changements LinkedIn. Réservé aux données non couvertes par les endpoints standard.

## Exemple
Voir `scripts/profile_views/` (parser wvmpCards réel).
