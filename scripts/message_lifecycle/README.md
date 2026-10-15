# 🔵 message_lifecycle (F5)

Service temps réel : reçoit les webhooks de cycle de vie des messages (lu, livré, réaction,
édité, supprimé) et les journalise. Point d'extension `record()` (store/dashboard).

- **Cadence** : récurrent (service always-on).
- **Évènements** : `message_read`, `message_delivered`, `message_reaction`, `message_edited`, `message_deleted`.

## Déployer (Modal)

```bash
modal deploy scripts/message_lifecycle/app.py
```

Puis enregistrer le webhook côté Unipile (`POST /webhooks`) sur l'URL renvoyée.
