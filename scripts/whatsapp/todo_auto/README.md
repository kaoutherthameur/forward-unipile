# 🔵 whatsapp/todo_auto (G3)

Chaque message WhatsApp entrant qui appelle une action ("tu peux m'envoyer", "il faudrait", "n'oublie pas") crée automatiquement une tâche dans votre outil.

- **Cadence** : récurrent (webhook, service always-on).
- **Évènement** : webhook `message_received`.
- **Logique** : `is_actionable(text)` (pure, testable) détecte l'intention d'action ;
  `process_event()` (pure) ignore vos messages sortants et les évènements non pertinents ;
  `create_task()` est le point d'extension (Notion / tasks.md / Todoist).

## Endpoints

- Reçu : webhook Unipile `message_received` (`{event, chat_id, message_id, message, sender}`).
- Aucune écriture WhatsApp : le service ne fait que lire l'évènement et créer une tâche ailleurs.

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/todo_auto/app.py
# -> renvoie une URL d'endpoint, ex. https://xxx--whatsapp-todo-auto-webhook.modal.run
```

Le secret Modal `unipile` doit porter `UNIPILE_OWN_PROVIDER_IDS` (vos provider_id WhatsApp, séparés par des virgules).

## Enregistrer le webhook côté Unipile

```python
from lib import unipile_helpers as u
u.post("webhooks", json={
    "request_url": "https://xxx--whatsapp-todo-auto-webhook.modal.run",
    "name": "whatsapp-todo-auto",
    "source": "messaging",
})
```

## Tester localement

```bash
python scripts/whatsapp/todo_auto/app.py   # importe sans modal ; is_actionable() est testable hors-ligne
```

## Exemple

`examples/whatsapp-todo_auto.md` (messages -> tâches créées, fictif).
