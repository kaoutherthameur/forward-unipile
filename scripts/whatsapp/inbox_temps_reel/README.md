# 🔵 whatsapp/inbox_temps_reel (A1)

Reçoit chaque message WhatsApp entrant et le pousse vers Slack/CRM. Les messages
sortants (les vôtres) sont filtrés via `UNIPILE_OWN_PROVIDER_IDS`. La fonction
`notify()` est un stub à câbler (webhook Slack, fiche CRM, etc.). Lecture seule.

- **Cadence** : récurrent (webhook `message_received`).
- **Endpoints** : webhook Unipile `message_received` (aucun appel sortant).
- **Garde-fous** : lecture seule (aucun envoi). Filtrage des messages sortants via `UNIPILE_OWN_PROVIDER_IDS`.

## Lancer (simulé)

Fonction pure testable hors-ligne (pas d'appel réseau) :

```python
from scripts.whatsapp.inbox_temps_reel.app import process_event
process_event({"event": "message_received", "chat_id": "c1",
               "sender": {"attendee_provider_id": "33600000000@s.whatsapp.net",
                          "attendee_name": "Camille Lefevre"},
               "message": "Bonjour, vous êtes ouverts samedi ?"}, set())
```

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/inbox_temps_reel/app.py
```

Puis enregistrer l'URL renvoyée comme webhook `message_received` côté Unipile
(`POST /webhooks`). Câbler `notify()` à votre Slack/CRM.
