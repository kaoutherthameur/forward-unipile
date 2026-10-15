# 🔵 entreprises_qui_recrutent (C2)

Recherche les offres d'emploi LinkedIn correspondant à des mots-clés/lieux et produit
un CSV de signaux (entreprise + offre). Lecture seule.

- **Cadence** : récurrent (cron hebdo).
- **Endpoint** : `POST /linkedin/search` (`category: jobs`).
- **Usage** : prospection (une boîte qui recrute un poste IA structure sa fonction) ou veille RH.

## Lancer

```bash
python scripts/entreprises_qui_recrutent/run.py --config scripts/entreprises_qui_recrutent/config.example.yaml
```

## Déployer (Modal, cron hebdo)

```python
@app.function(image=image, schedule=modal.Cron("0 4 * * 1"), secrets=[modal.Secret.from_name("unipile")])
def weekly():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Enchaîner ensuite avec `unipile-enrichir-liste` (trouver le décideur) puis `invitation_drip`.
