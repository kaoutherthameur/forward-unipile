# 🔵 engagement_cible (D3)

Réagit (like, etc.) à une liste de posts ciblés - nurturing sur des comptes cibles.
**Écriture** : simulé par défaut (`UNIPILE_DRY_RUN=1`). Garde-fous : plafond/jour, jitter.

- **Cadence** : récurrent (cron).
- **Endpoint** : `POST /posts/{social_id}/reactions`.

## Lancer (simulé)

```bash
python scripts/engagement_cible/run.py --config scripts/engagement_cible/config.example.yaml
```

## Déployer (Modal, cron)

```python
@app.function(image=image, schedule=modal.Cron("0 9 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

À utiliser avec parcimonie : l'engagement automatique générique se repère.
