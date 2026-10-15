# 🔵 whatsapp/tri_demandes (A3)

Classe chaque message WhatsApp entrant en `sav` / `commande` / `reservation` /
`spam` / `autre` via `classify()` (fonction pure, mots-clés) et le route vers le
bon canal via `route_to()` (stub à câbler). Lecture seule.

- **Cadence** : récurrent (webhook `message_received`).
- **Endpoints** : webhook Unipile `message_received` (aucun appel sortant).
- **Garde-fous** : lecture seule (aucun envoi). Filtrage des messages sortants via `UNIPILE_OWN_PROVIDER_IDS`.

## Lancer (simulé)

Fonction pure testable hors-ligne :

```python
from scripts.whatsapp.tri_demandes.app import classify
classify("Mon colis n'est pas arrivé")        # -> "commande"
classify("Je voudrais réserver une table")    # -> "reservation"
classify("Vous avez gagné un iPhone, cliquez ici")  # -> "spam"
```

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/tri_demandes/app.py
```

Enregistrer l'URL comme webhook `message_received` côté Unipile (`POST /webhooks`).
Câbler `route_to()` à vos outils (file SAV, outil commandes, agenda, corbeille spam).
