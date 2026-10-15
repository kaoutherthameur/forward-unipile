# 🔵 whatsapp/rappel_rdv (C1)

Envoie un rappel de rendez-vous à **J-1** puis à **H-2**, pour réduire le no-show.
Compte WhatsApp perso connecté à Unipile (QR). **Écriture simulée par défaut** (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron, plusieurs fois par jour, ex. toutes les 2 heures).
- **Endpoints** : `POST /chats/{id}/messages` (envoi du rappel).
- **Idempotence** : clé stable `(chat_id, étape, jour de l'étape)` ; un rappel déjà envoyé n'est jamais réémis.
- **Garde-fous** : plafond quotidien (`u.daily_cap()`), fenêtre horaire locale (`u.in_send_window()`), jitter (`u.sleep_jitter()`) avant chaque envoi.

WhatsApp perso bannit vite le volume : rester déclenché et opt-in (le contact a pris rendez-vous et attend ce rappel).

## Lancer (simulé)

```bash
python scripts/whatsapp/rappel_rdv/run.py --config scripts/whatsapp/rappel_rdv/config.example.yaml
```

La fonction `reminders_due(appointments, now)` est pure et testable hors-ligne (aucun appel réseau).

## Déployer (Modal)

```python
@app.function(image=image, schedule=modal.Cron("30 5 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Astuce : pour bien capter la fenêtre H-2, planifier plusieurs passages dans la journée (ex. `modal.Cron("0 */2 * * *")`).
