# 🔵 nettoyer_invitations (B5)

Retire les invitations envoyées et restées en attente depuis plus de N jours, pour
libérer le quota hebdomadaire LinkedIn. **Écriture** : simulé par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron hebdo).
- **Endpoints** : `GET /users/invitations/sent`, `DELETE /users/invite/{id}`.

## Lancer (simulé)

```bash
python scripts/nettoyer_invitations/run.py --config scripts/nettoyer_invitations/config.example.yaml
```

## Déployer (Modal, cron hebdo)

```python
@app.function(image=image, schedule=modal.Cron("0 6 * * 1"), secrets=[modal.Secret.from_name("unipile")])
def weekly():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```
