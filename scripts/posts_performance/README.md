# 🔵 posts_performance (D4)

Snapshot quotidien de la performance de vos posts LinkedIn : impressions, réactions,
commentaires, reposts, + **visiteurs de profil** et **followers gagnés** générés par chaque post.

- **Cadence** : récurrent (cron quotidien).
- **Lecture seule** (aucune écriture, pas de risque de ban).
- **Endpoints** : `GET /users/me`, `GET /users/{identifier}/posts`, `GET /posts/{social_id}`.

## Lancer

```bash
python scripts/posts_performance/run.py --config scripts/posts_performance/config.example.yaml
```

Produit un CSV daté (`captured_at`). Relancé chaque jour, il bâtit une série temporelle.

## Déployer (Modal, cron)

```python
# deploy.py (exemple)
import modal
app = modal.App("posts-performance")
image = modal.Image.debian_slim().pip_install("httpx", "python-dotenv", "pyyaml")

@app.function(image=image, schedule=modal.Cron("0 7 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

`modal deploy deploy.py`. Le secret `unipile` doit porter `UNIPILE_DSN`, `UNIPILE_API_KEY`, `UNIPILE_ACCOUNT_ID`.

## Voir aussi

Exemple de sortie : `examples/posts-performance.csv`.
