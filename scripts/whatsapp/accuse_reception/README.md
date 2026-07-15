# 🔵 whatsapp/accuse_reception (A4)

Envoie un accusé de réception automatique quand un message WhatsApp arrive **hors
des heures d'ouverture** (`u.in_send_window(pays)` renvoie `False`). Dans la fenêtre
d'ouverture, aucun accusé n'est envoyé (un humain répond en direct).

Écriture simulée par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (webhook `message_received`).
- **Endpoints** : `POST /chats/{id}/messages` (envoi de l'accusé).
- **Garde-fous** : envoi `is_write=True` + `UNIPILE_DRY_RUN` par défaut. Envoi uniquement hors fenêtre horaire (un seul accusé par message entrant). Filtrage des messages sortants via `UNIPILE_OWN_PROVIDER_IDS`.

## Lancer (simulé)

Fonction pure testable hors-ligne (`in_window` injecté, pas d'appel réseau) :

```python
from scripts.whatsapp.accuse_reception.app import process_event
# message reçu à 23h (hors fenêtre) -> accusé
process_event({"event": "message_received", "chat_id": "c1",
               "sender": {"attendee_provider_id": "x"}}, set(), in_window=False)
# message reçu à 14h (dans la fenêtre) -> ignore
process_event({"event": "message_received", "chat_id": "c1",
               "sender": {"attendee_provider_id": "x"}}, set(), in_window=True)
```

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/accuse_reception/app.py
```

Enregistrer l'URL comme webhook `message_received` côté Unipile (`POST /webhooks`).
Régler `UNIPILE_SEND_COUNTRY` et `WHATSAPP_ACK_TEXT` dans le secret Modal `unipile`.
