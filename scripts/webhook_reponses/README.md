# 🔵 webhook_reponses (F2)

Service temps réel : reçoit les webhooks Unipile `message_received`, filtre les messages
**entrants** (pas les vôtres) et notifie en quelques secondes (Slack/log/CRM).

- **Cadence** : récurrent (service always-on).
- **Évènement** : webhook `message_received`.
- **Logique** : `process_event()` (pure, testable) ignore vos messages sortants et les
  évènements non pertinents ; `notify()` est le point d'extension (Slack/email/CRM).

## Déployer (Modal)

```bash
modal deploy scripts/webhook_reponses/app.py
# -> renvoie une URL d'endpoint, ex. https://xxx--unipile-webhook-reponses-webhook.modal.run
```

Le secret Modal `unipile` doit porter `UNIPILE_OWN_PROVIDER_IDS` (vos provider_id, séparés par des virgules).

## Enregistrer le webhook côté Unipile

```python
from lib import unipile_helpers as u
u.post("webhooks", json={
    "request_url": "https://xxx--unipile-webhook-reponses-webhook.modal.run",
    "name": "linkedin-replies",
    "source": "messaging",
})
```

## Tester localement

```bash
python scripts/webhook_reponses/app.py   # importe sans modal ; voir tests dans le repo
```
