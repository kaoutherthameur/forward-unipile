# 🔵 whatsapp/relance_devis (C2)

Relance en douceur un **devis ou une facture** envoyé et resté sans réponse, à J+N.
Compte WhatsApp perso connecté à Unipile (QR). **Écriture simulée par défaut** (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron quotidien, ex. 07:30).
- **Endpoints** : `POST /chats/{id}/messages` (envoi de la relance).
- **Idempotence** : clé stable `(chat_id, palier en jours)` ; un seul envoi par palier.
- **Garde-fous** : plafond quotidien (`u.daily_cap()`), fenêtre horaire locale (`u.in_send_window()`), jitter (`u.sleep_jitter()`) avant chaque envoi.

WhatsApp perso bannit vite le volume : rester déclenché et opt-in (le contact a demandé le devis).

## Lancer (simulé)

```bash
python scripts/whatsapp/relance_devis/run.py --config scripts/whatsapp/relance_devis/config.example.yaml
```

Les fonctions `due_for_followup(sent_at, now, days)` et `followups_due(...)` sont pures et testables hors-ligne.

## Déployer (Modal)

```python
@app.function(image=image, schedule=modal.Cron("30 5 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Règle : au dernier palier, on s'arrête (on ne harcèle pas - respect du temps du prospect).
