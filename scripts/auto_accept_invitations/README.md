# 🔵 auto_accept_invitations (B6)

Accepte les invitations entrantes et envoie un message de bienvenue. **Écriture** :
simulé par défaut (`UNIPILE_DRY_RUN=1`). Garde-fous : plafond/jour, jitter.

- **Cadence** : récurrent (cron quotidien).
- **Endpoints** : `GET /users/invitations/received`, `PATCH /users/invitations/{id}`, `POST /chats`.

## Lancer (simulé)

```bash
python scripts/auto_accept_invitations/run.py --config scripts/auto_accept_invitations/config.example.yaml
```

## Déployer (Modal, cron quotidien)

```python
@app.function(image=image, schedule=modal.Cron("0 8 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```
