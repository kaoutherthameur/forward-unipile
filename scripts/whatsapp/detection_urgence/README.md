# 🔵 whatsapp/detection_urgence (A6)

Analyse chaque message WhatsApp entrant et lève une **alerte prioritaire** dès qu'un
signal de churn/urgence est détecté (`is_urgent()` : "annuler", "remboursement",
"déçu", "urgent", "inadmissible", etc.). `alert()` est un stub à câbler. Lecture seule.

- **Cadence** : récurrent (webhook `message_received`).
- **Endpoints** : webhook Unipile `message_received` (aucun appel sortant).
- **Garde-fous** : lecture seule (aucun envoi). Filtrage des messages sortants via `UNIPILE_OWN_PROVIDER_IDS`.

## Lancer (simulé)

Fonctions pures testables hors-ligne :

```python
from scripts.whatsapp.detection_urgence.app import is_urgent, matched_keywords
is_urgent("Je veux annuler et être remboursé, c'est inadmissible")  # -> True
matched_keywords("Je veux annuler et être remboursé")  # -> ["annuler", "remboursement", ...]
is_urgent("Merci beaucoup pour votre aide !")  # -> False
```

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/detection_urgence/app.py
```

Enregistrer l'URL comme webhook `message_received` côté Unipile (`POST /webhooks`).
Câbler `alert()` à un canal prioritaire (Slack `#urgences-support`, CRM, SMS responsable).
