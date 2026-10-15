# 🔵 whatsapp/relance_panier (C5)

Envoie **un rappel unique** après un panier ou une réservation abandonné (événements fournis en entrée).
Compte WhatsApp perso connecté à Unipile (QR). **Écriture simulée par défaut** (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron plusieurs fois par jour, ex. toutes les 2 heures pour tenir le délai court).
- **Endpoints** : `POST /chats/{id}/messages` (envoi du rappel).
- **Idempotence** : clé stable `(chat_id, event_id)` ; un rappel déjà envoyé n'est jamais réémis.
- **Garde-fous** : plafond quotidien (`u.daily_cap()`), fenêtre horaire locale (`u.in_send_window()`), jitter (`u.sleep_jitter()`) avant chaque envoi.

WhatsApp perso bannit vite le volume : rester déclenché et opt-in (le contact a initié l'achat et vous a déjà écrit).

## Lancer (simulé)

```bash
python scripts/whatsapp/relance_panier/run.py --config scripts/whatsapp/relance_panier/config.example.yaml
```

Les fonctions `eligible_for_reminder(abandoned_at, now)` et `reminders_due(...)` sont pures et testables hors-ligne.

## Déployer (Modal)

```python
@app.function(image=image, schedule=modal.Cron("30 5 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Délai court (quelques heures) : planifier plusieurs passages, ex. `modal.Cron("0 */2 * * *")`.
