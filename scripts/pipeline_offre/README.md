# 🔵 pipeline_offre (C5)

Liste les candidats d'une offre LinkedIn (et signale les CV disponibles). Lecture seule.

- **Cadence** : récurrent (cron, tant que le poste est ouvert).
- **Endpoints** : `GET /linkedin/jobs/{id}/applicants`, `GET /linkedin/jobs/{id}/applicants/{aid}/resume`.
- **Prérequis** : compte Recruiter.

## Lancer

```bash
python scripts/pipeline_offre/run.py --config scripts/pipeline_offre/config.example.yaml
```

Le CSV signale `resume_available` ; télécharger le CV via l'endpoint `.../resume`.

## Déployer (Modal, cron quotidien)

```python
@app.function(image=image, schedule=modal.Cron("0 7 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```
