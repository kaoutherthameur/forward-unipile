# 🔵 warm_touch (E6)

Déclenche une **visite de profil visible** (`notify=true`) sur une liste de cibles : elles
voient votre passage dans "qui a vu votre profil" - une touche douce avant outreach.
Traité comme une écriture : simulé par défaut (`UNIPILE_DRY_RUN=1`), garde-fous fenêtre + cap + jitter.

- **Cadence** : récurrent (cron drip quotidien).
- **Endpoint** : `GET /users/{id}` avec `notify=true`.

## Lancer (simulé)

```bash
python scripts/warm_touch/run.py --config scripts/warm_touch/config.example.yaml
```

## Déployer (Modal, cron quotidien)

```python
@app.function(image=image, schedule=modal.Cron("0 10 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```
