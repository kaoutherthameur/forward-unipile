# 🔵 approche_candidats (C3)

Approche automatisée de candidats : invitation + note, ou InMail Recruiter si hors réseau.
**Écriture** : simulé par défaut (`UNIPILE_DRY_RUN=1`). Garde-fous : plafond/jour, fenêtre locale, jitter.

- **Cadence** : récurrent (cron).
- **Endpoints** : `GET /users/{id}`, `POST /users/invite`, `POST /chats` (inmail recruiter).
- Alimenter `candidates` depuis la skill `unipile-sourcing-candidats`.

## Lancer (simulé)

```bash
python scripts/approche_candidats/run.py --config scripts/approche_candidats/config.example.yaml
```

## Déployer (Modal, cron)

```python
@app.function(image=image, schedule=modal.Cron("0 8 * * 1-5"), secrets=[modal.Secret.from_name("unipile")])
def weekday():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```
