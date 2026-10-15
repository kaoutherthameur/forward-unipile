---
name: unipile-exporter-reseau
description: Use when you want to export your full LinkedIn 1st-degree network to CSV (backup, analysis, CRM import). No input -> CSV of connections.
---
# Exporter tout votre réseau LinkedIn

## Objectif & quand
One-shot : exporter la liste de vos connexions 1er degré (backup, analyse, import CRM).

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `output_path` | CSV de sortie |

## Procédure (via MCP)
1. Demander la liste des relations (`GET /users/relations`), paginer via `cursor`.
2. Mapper chaque relation et écrire le CSV.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
relations = list(u.paginate("users/relations"))
```

## Livrable
CSV : `name, headline, profile_url, connected_at`.

## Limites & anti-ban
Lecture seule. La pagination peut être longue sur un gros réseau.

## Exemple
`examples/exporter-reseau.csv` (données fictives, schéma réel).
