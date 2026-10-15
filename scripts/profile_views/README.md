# 🔵 profile_views (E1)

Récupère les **visiteurs identifiés** de votre profil LinkedIn (qui a vu votre profil) via
le proxy raw Voyager d'Unipile (`wvmpCards`). Lecture seule.

- **Cadence** : récurrent (cron quotidien - LinkedIn ne garde qu'une fenêtre glissante).
- **Endpoint** : `POST /linkedin` (getRawData proxy vers `/voyager/api/identity/wvmpCards`).
- **Note** : seul endpoint qui renvoie les NOMS (les endpoints publics renvoient l'anonyme). Premium recommandé pour la liste complète.

## Lancer

```bash
python scripts/profile_views/run.py --config scripts/profile_views/config.example.yaml
```

## Déployer (Modal, cron quotidien)

```python
@app.function(image=image, schedule=modal.Cron("0 6 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Enchaîner avec `unipile-enrichir-liste` pour qualifier les visiteurs, ou un CRM.
