# 🔵 whatsapp/checkin_quotidien (E1)

Envoie chaque matin un message de check-in WhatsApp à chaque coaché opt-in listé en
config ("C'est fait, ton action du jour ?"). Le message est composé par la fonction
pure `build_checkin()` (rotation de templates + prénom + action du jour).

Écriture simulée par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron, une fois le matin).
- **Endpoints** : `POST /chats/{id}/messages` (envoi du check-in dans le fil existant).
- **Garde-fous** : envoi `is_write=True` + `UNIPILE_DRY_RUN` par défaut. Plafond quotidien (`u.daily_cap()`), fenêtre d'envoi locale (`u.in_send_window()`), pause aléatoire (`u.sleep_jitter()`). Envois OPT-IN uniquement (coachés ayant accepté le suivi).

## Lancer (simulé)

```bash
python scripts/whatsapp/checkin_quotidien/run.py --config scripts/whatsapp/checkin_quotidien/config.example.yaml
```

Fonction pure testable hors-ligne :

```python
from scripts.whatsapp.checkin_quotidien.run import build_checkin
build_checkin({"prenom": "Camille", "action_du_jour": "30 min de rédaction"}, ["Salut {prenom} ! {action} ?"])
```

## Déployer (Modal)

Programmer l'exécution matinale via un cron Modal :

```python
import modal

app = modal.App("whatsapp-checkin_quotidien")
image = modal.Image.debian_slim().pip_install("httpx", "pyyaml", "python-dotenv")

@app.function(image=image, secrets=[modal.Secret.from_name("unipile")], schedule=modal.Cron("0 7 * * *"))
def daily():
    from scripts.whatsapp.checkin_quotidien.run import run
    from lib import unipile_helpers as u
    run(u.load_config("scripts/whatsapp/checkin_quotidien/config.example.yaml"))
```

Compte perso : garder le volume bas et déclenché par un vrai suivi. Passer
`UNIPILE_DRY_RUN=0` seulement une fois la liste opt-in vérifiée.
