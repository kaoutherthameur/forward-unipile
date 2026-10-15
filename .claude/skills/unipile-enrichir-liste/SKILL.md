---
name: unipile-enrichir-liste
description: Use when you have a CSV of LinkedIn profile URLs/slugs and want them enriched (title, company, location, network distance, followers, email if visible). CSV in -> enriched CSV out.
---
# Enrichir une liste de prospects LinkedIn

## Objectif & quand
One-shot : tu as une liste de profils LinkedIn (URLs ou slugs) et tu veux la compléter avec les données du profil pour qualifier/scorer avant outreach ou import CRM.

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic suffit).
- MCP Unipile configuré (`CONNECTING-MCP.md`).
- Un CSV d'entrée avec une colonne `linkedin` (URL ou slug).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `input_path` | CSV d'entrée (colonne `linkedin`) |
| `output_path` | CSV enrichi de sortie |
| `notify` | si true, déclenche une visite de profil (la cible le voit). Défaut: false |

## Procédure (via MCP)
1. Lire le CSV d'entrée. Pour chaque ligne, extraire le slug (`public_identifier`) depuis l'URL.
2. Demander au MCP le profil (`GET /users/{identifier}`).
3. Mapper les champs (voir Livrable). Espacer les appels (lecture, mais reste raisonnable : ~80-100 profils/jour en Classic).
4. Écrire le CSV enrichi.

## Si le MCP ne fait pas l'action
Fallback REST (lecture) via `lib/unipile_helpers.py` :
```python
from lib import unipile_helpers as u
prof = u.get(f"users/{u.encode_urn(slug)}")
```
Champs profil utiles : `first_name`, `last_name`, `headline`, `location`, `primary_locale.country`,
`network_distance`, `is_premium`, `follower_count`, `connections_count`, `contact_info.emails`,
`public_identifier`.

## Livrable
CSV : `linkedin, name, headline, location, country, network_distance, is_premium, follower_count, connections_count, email, public_identifier`.

## Limites & anti-ban
Lecture, mais respecte ~80-100 profils/jour (Classic) / 150 (Sales Nav). `notify=true` rend la visite visible par la cible (utile pour un "warm touch", à activer en connaissance de cause). Email présent seulement s'il est visible sur le profil.

## Exemple
`examples/enrichir-liste.csv` (données fictives, schéma réel).
