# 🔵 monitoring_comptes (G4)

Service temps réel : reçoit le webhook `account_status` et alerte si un compte se
déconnecte ou tombe sur un checkpoint - pour réagir avant que les workflows ne cassent.
`alert()` est un stub (Slack/email) à câbler.

- **Cadence** : récurrent (service always-on).
- **Évènement** : `account_status`. Reconnexion : `POST /accounts/{id}/reconnect`.

## Déployer (Modal)

```bash
modal deploy scripts/monitoring_comptes/app.py
```

Puis `POST /webhooks` côté Unipile sur l'URL renvoyée.
