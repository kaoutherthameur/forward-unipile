# 🔵 endorse_nurturing (E5)

Endosse des compétences de contacts cibles (nurturing relationnel léger). **Écriture** :
simulé par défaut (`UNIPILE_DRY_RUN=1`). Garde-fous : plafond quotidien, jitter.

- **Cadence** : récurrent (cron).
- **Endpoint** : `POST /linkedin/skills/{id}/endorse`.

## Lancer (simulé)

```bash
python scripts/endorse_nurturing/run.py --config scripts/endorse_nurturing/config.example.yaml
```

Les `skill_id` se récupèrent depuis le profil de la cible (`GET /users/{id}`).

## Déployer (Modal, cron)

```python
@app.function(image=image, schedule=modal.Cron("0 9 * * 2"), secrets=[modal.Secret.from_name("unipile")])
def weekly():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```
