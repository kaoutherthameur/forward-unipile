# 🔵 whatsapp/onboarding_client (C3)

Déroule une **séquence d'onboarding post-achat** : J0 (bienvenue), J+2 (conseil), J+7 (check).
Compte WhatsApp perso connecté à Unipile (QR). **Écriture simulée par défaut** (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron quotidien, ex. 07:30).
- **Endpoints** : `POST /chats/{id}/messages` (envoi du message de l'étape).
- **Idempotence** : clé stable `(client, étape)` ; une étape déjà envoyée n'est jamais réémise.
- **Garde-fous** : plafond quotidien (`u.daily_cap()`), fenêtre horaire locale (`u.in_send_window()`), jitter (`u.sleep_jitter()`) avant chaque envoi.

WhatsApp perso bannit vite le volume : rester déclenché et opt-in (le client vient d'acheter).

## Lancer (simulé)

```bash
python scripts/whatsapp/onboarding_client/run.py --config scripts/whatsapp/onboarding_client/config.example.yaml
```

La fonction `step_due(signup_at, now, steps)` est pure et testable hors-ligne (renvoie l'étape du jour, ou `None`).

## Déployer (Modal)

```python
@app.function(image=image, schedule=modal.Cron("30 5 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Un cron **quotidien** suffit : au plus une étape par client et par jour.
