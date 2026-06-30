# 🔵 social_listening (A5)

Recherche les posts LinkedIn récents sur des mots-clés et produit un CSV (auteur,
engagement, lien) - pour repérer qui parle d'un sujet et l'engager. Lecture seule.

- **Cadence** : récurrent (cron, ex. quotidien).
- **Endpoint** : `POST /linkedin/search` (`category: posts`).

## Lancer

```bash
python scripts/social_listening/run.py --config scripts/social_listening/config.example.yaml
```

## Déployer (Modal, cron)

```python
@app.function(image=image, schedule=modal.Cron("0 7 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Enchaîner avec `unipile-engageurs-post` (les engageurs des posts trouvés) ou `unipile-enrichir-liste`.
