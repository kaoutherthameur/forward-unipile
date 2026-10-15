# 🔵 sync_connexions_crm (G1)

Service temps réel : reçoit le webhook `new_relation` (connexion acceptée) et crée une
fiche dans votre CRM. **CRM générique** : la fonction `to_crm()` est un stub à câbler
(Attio, HubSpot, Google Sheet, etc.).

- **Cadence** : récurrent (service always-on). Note : `new_relation` peut avoir jusqu'à 8h de délai côté LinkedIn.
- **Évènement** : `new_relation`.

## Déployer (Modal)

```bash
modal deploy scripts/sync_connexions_crm/app.py
```

Puis `POST /webhooks` côté Unipile sur l'URL renvoyée. Câbler `to_crm()` à votre CRM
(+ éventuel message de bienvenue via `POST /chats`).
