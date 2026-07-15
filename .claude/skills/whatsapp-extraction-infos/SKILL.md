---
name: whatsapp-extraction-infos
description: Use when you want to turn WhatsApp conversations into structured data (adresses, montants, dates de RDV, coordonnées). Conversations -> CSV prêt pour un tableur/CRM.
---
# Extraction d'infos structurées depuis WhatsApp

## Objectif & quand
One-shot : transformer des conversations WhatsApp en tableau exploitable. Claude parcourt les échanges et extrait les informations utiles (adresses, montants, dates de rendez-vous, coordonnées, références de commande) vers un CSV directement importable dans un tableur ou un CRM.

## Prérequis
- Compte(s) WhatsApp connecté(s) à Unipile (QR). MCP Unipile configuré (`CONNECTING-MCP.md`).

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `info_types` | types d'infos à extraire (adresse, montant, date_rdv, coordonnees, reference) |
| `contacts_input` | facultatif : CSV de contacts à cibler (`input.example.csv`). Vide = toutes les conversations |
| `limit_chats` | nombre de conversations à balayer |
| `messages_per_chat` | profondeur d'historique par conversation |
| `output_path` | CSV de sortie |

## Procédure (via MCP)
1. Lister les conversations WhatsApp (`GET /chats`, provider WhatsApp), paginer jusqu'à `limit_chats`.
2. Si `contacts_input` est fourni, ne garder que les conversations des contacts listés (résolution via `GET /chat_attendees`).
3. Pour chaque conversation, lire l'historique (`GET /chats/{id}/messages`) jusqu'à `messages_per_chat`.
4. Extraire les informations demandées dans `info_types` (une ligne CSV par info trouvée), en gardant le message source et sa date.
5. Dédupliquer (même contact + même type + même valeur) et écrire le CSV.

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
chats = list(u.paginate("chats", params={"provider": "WHATSAPP"}, max_items=50))
rows = []
for c in chats:
    for m in u.paginate(f"chats/{c['id']}/messages", max_items=200):
        # détecter montants / adresses / dates dans (m.get("text") or "")
        pass
u.write_csv("examples/whatsapp-extraction-infos.csv", rows,
            fieldnames=["contact", "type_info", "valeur", "source_message", "date"])
```

## Livrable
CSV avec les colonnes : `contact`, `type_info`, `valeur`, `source_message`, `date`. Une ligne par information extraite, prête à importer dans un tableur ou un CRM.

## Limites & anti-ban
Lecture seule (aucune écriture WhatsApp). Compte perso : consultation uniquement. L'extraction reste probabiliste (Claude interprète le texte libre) : relire les montants et coordonnées avant de les pousser dans un CRM.

## Exemple
`examples/whatsapp-extraction-infos.csv` (données fictives, colonnes réelles).
