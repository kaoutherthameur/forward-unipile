# 🔵 invitation_drip (B1)

Envoie un **drip quotidien d'invitations** LinkedIn + note personnalisée à une liste de
cibles, avec garde-fous anti-ban. **Écriture** : simulé par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron quotidien).
- **Endpoints** : `GET /users/{identifier}` (degré + provider_id), `POST /users/invite`.
- **Garde-fous** : plafond quotidien, fenêtre horaire locale [07:30-19:30], jitter, skip des 1er degré.

## Lancer (simulé)

```bash
python scripts/invitation_drip/run.py --config scripts/invitation_drip/config.example.yaml
# UNIPILE_DRY_RUN=1 (défaut) -> aucune invitation réelle, tout est loggé en [DRY_RUN]
```

Passer en réel : `UNIPILE_DRY_RUN=0` (à tes risques, respecte les quotas LinkedIn).

## Alimenter les cibles

`targets` peut être rempli à la main, ou généré par la skill `unipile-prospects-salesnav`
(exporte une recherche en CSV, puis convertis en `targets`).

## Déployer (Modal, cron quotidien)

```python
@app.function(image=image, schedule=modal.Cron("0 8 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

## Limites LinkedIn

Invitations : ~100-200/semaine selon le compte ; les invitations **avec note** sont plus
limitées (garde la note courte et rare). Le plafond `UNIPILE_DAILY_CAP` borne chaque run.
