# 🔵 whatsapp/demande_avis (C4)

Envoie, **X jours après une prestation**, une demande de note + un lien d'avis Google.
Compte WhatsApp perso connecté à Unipile (QR). **Écriture simulée par défaut** (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron quotidien, ex. 07:30).
- **Endpoints** : `POST /chats/{id}/messages` (envoi de la demande).
- **Idempotence** : clé stable `(chat_id, avis)` ; une demande déjà envoyée n'est jamais réémise.
- **Garde-fous** : plafond quotidien (`u.daily_cap()`), fenêtre horaire locale (`u.in_send_window()`), jitter (`u.sleep_jitter()`) avant chaque envoi.

WhatsApp perso bannit vite le volume : rester déclenché et opt-in (le client vient d'être livré).

## Lancer (simulé)

```bash
python scripts/whatsapp/demande_avis/run.py --config scripts/whatsapp/demande_avis/config.example.yaml
```

Les fonctions `eligible_for_review(done_at, now)` et `build_message(template, lien)` sont pures et testables hors-ligne.

## Déployer (Modal)

```python
@app.function(image=image, schedule=modal.Cron("30 5 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Une seule demande par client : au-delà de la fenêtre, on n'insiste pas.
