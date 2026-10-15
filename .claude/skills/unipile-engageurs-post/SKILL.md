---
name: unipile-engageurs-post
description: Use when you want the people who liked/commented a LinkedIn post (yours, a competitor's, an influencer's) as a qualified lead list. Post URL -> CSV of engagers.
---
# Engageurs d'un post LinkedIn -> liste de leads

## Objectif & quand
One-shot : tu as un post LinkedIn (le tien, celui d'un concurrent ou d'un influenceur) et tu veux la liste des gens qui ont **réagi** et **commenté** - une liste chaude à exploiter en outreach.

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic suffit).
- MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `post_url` | URL du post LinkedIn (ou directement le `social_id` URN) |
| `include_reactions` | inclure les réacteurs (défaut: true) |
| `include_comments` | inclure les commentateurs (défaut: true) |
| `output_path` | chemin du CSV de sortie |

## Procédure (via MCP)
1. Déduire le `social_id` (URN) du post depuis l'URL :
   - `.../activity/<ID>` -> `urn:li:activity:<ID>` · `.../ugcPost/<ID>` -> `urn:li:ugcPost:<ID>` · `.../share/<ID>` -> `urn:li:share:<ID>`.
2. Demander au MCP la liste des **réactions** du post (`GET /posts/{social_id}/reactions`) - pagine tout.
3. Demander la liste des **commentaires** (`GET /posts/{social_id}/comments`) - pagine tout.
4. Fusionner en lignes : une ligne par (personne, type d'engagement). Dédupe sur l'id auteur si tu veux une personne unique.
5. Écrire le CSV (colonnes ci-dessous).

## Si le MCP ne fait pas l'action
Fallback REST (lecture) via `lib/unipile_helpers.py` :
```python
from lib import unipile_helpers as u
sid = u.encode_urn("urn:li:activity:7457342077836767232")
reactions = list(u.paginate(f"posts/{sid}/reactions"))
comments  = list(u.paginate(f"posts/{sid}/comments"))
```
Champs utiles : réaction -> `value`, `author.{name,headline,profile_url,network_distance}` ; commentaire -> `text`, `author_details.{headline,profile_url,network_distance}`, `author` (nom).

## Livrable
CSV : `name, headline, engagement_type, reaction_value, comment_preview, network_distance, profile_url`.

## Limites & anti-ban
Lecture seule (pas de risque d'écriture). Pense à paginer jusqu'au bout (`total_count` dans `paging`). Les profils 2e/3e degré peuvent avoir un `profile_url` anonymisé (slug `ACoAA...`).

## Exemple
`examples/engageurs-post.csv` (données fictives, schéma réel).
