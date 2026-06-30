# 🔵 relance_j3 (B3)

Relance **une seule fois** les prospects contactés il y a 3 à 7 jours et restés silencieux.
**Écriture** : simulé par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron quotidien, ex. 07:30).
- **Endpoints** : `GET /chats/{id}/messages` (anti-collision), `POST /chats/{id}/messages`.
- **Anti-collision** : relit la conversation et n'envoie pas si le prospect a déjà répondu.
- **Garde-fous** : plafond quotidien, fenêtre horaire locale, jitter.

## Lancer (simulé)

```bash
python scripts/relance_j3/run.py --config scripts/relance_j3/config.example.yaml
```

## Déployer (Modal, cron quotidien)

```python
@app.function(image=image, schedule=modal.Cron("30 5 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Règle : **une seule relance** par lead (au-delà de J+7, on arrête - respect du temps du prospect).
