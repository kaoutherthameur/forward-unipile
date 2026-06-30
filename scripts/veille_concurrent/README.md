# 🔵 veille_concurrent (D5)

Digest périodique des posts récents d'un profil cible (concurrent, influenceur, prospect)
avec leur engagement. Lecture seule.

- **Cadence** : récurrent (cron hebdo/quotidien).
- **Endpoint** : `GET /users/{identifier}/posts`.

## Lancer

```bash
python scripts/veille_concurrent/run.py --config scripts/veille_concurrent/config.example.yaml
```

Produit un digest markdown (`examples/veille-concurrent.md`).

## Déployer (Modal, cron hebdo)

```python
@app.function(image=image, schedule=modal.Cron("0 8 * * 1"), secrets=[modal.Secret.from_name("unipile")])
def weekly():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Astuce : pour surveiller plusieurs profils, dupliquer la config (un fichier par cible)
ou itérer sur une liste d'`identifier`.
