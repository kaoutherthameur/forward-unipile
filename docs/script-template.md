# Moule : script workflow 🔵 (récurrent)

Un script = un dossier `scripts/{cas}/` avec :

```
scripts/{cas}/
  run.py               # contrat ci-dessous
  config.example.yaml  # config pré-remplie, sujet public/fictif
  README.md            # ce que ça fait + déploiement Modal (cron/webhook) + anti-ban
```

Le script appelle l'API REST via `lib/unipile_helpers.py` et se déploie en cron ou webhook
(Modal). Les écritures (invitation, DM) tournent en `DRY_RUN` par défaut.

## Contrat de `run.py`

```python
#!/usr/bin/env python3
"""[Cas] - [une phrase]. Récurrent (cron/webhook)."""
import os, sys, argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from dotenv import load_dotenv
load_dotenv()
from lib import unipile_helpers as u


def run(cfg):
    # 1. lire les entrées (recherche, liste, etc.) via u.get / u.paginate
    # 2. pour chaque action d'écriture : garde-fous AVANT l'appel
    #    - u.in_send_window(country) ?  -> sinon skip/queue
    #    - compteur < u.daily_cap() ?   -> sinon stop
    #    - u.sleep_jitter()             -> espacement aléatoire
    #    - u.post(..., is_write=True)   -> respecte UNIPILE_DRY_RUN
    # 3. journaliser chaque action (toujours)
    ...


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "config.example.yaml"))
    args = ap.parse_args()
    run(u.load_config(args.config))


if __name__ == "__main__":
    main()
```

## Règles

- **Toujours** : garde-fous anti-ban avant chaque écriture (`in_send_window`, `daily_cap`, `sleep_jitter`) ; `is_write=True` sur les POST d'écriture (respecte `DRY_RUN`) ; journaliser chaque action.
- **Déploiement** : `README.md` du script documente le déploiement Modal (cron via `modal deploy`, ou webhook via `@modal.web_endpoint`). L'utilisateur déploie sur SON Modal.
- **Idempotence** : pour les crons, dédupliquer (clé stable) pour ne pas réémettre. Pour les webhooks, répondre 200 vite et dédupliquer par id d'événement.
