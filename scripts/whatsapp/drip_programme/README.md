# 🔵 whatsapp/drip_programme (E3)

Délivre un programme de coaching au goutte-à-goutte sur WhatsApp : un module/exercice
par jour, pendant N jours. Pour chaque coaché, la fonction pure `module_for_day()`
calcule le module dû à partir de sa date de démarrage (`start_at`) et de la date du
jour. Pièce jointe possible par module (`attachment_url`).

Écriture simulée par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron, une fois par jour).
- **Endpoints** : `POST /chats/{id}/messages` (texte + `attachments` optionnels).
- **Garde-fous** : envoi `is_write=True` + `UNIPILE_DRY_RUN` par défaut. Plafond quotidien (`u.daily_cap()`), fenêtre locale (`u.in_send_window()`), jitter (`u.sleep_jitter()`). Idempotence sur (coaché, jour) via un journal local (`state_path`) : pas de double envoi si le cron repasse dans la journée.

## Lancer (simulé)

```bash
python scripts/whatsapp/drip_programme/run.py --config scripts/whatsapp/drip_programme/config.example.yaml
```

Fonction pure testable hors-ligne :

```python
from datetime import datetime, timezone
from scripts.whatsapp.drip_programme.run import module_for_day
mods = [{"jour": 1, "titre": "J1"}, {"jour": 2, "titre": "J2"}]
module_for_day("2026-07-14", datetime(2026, 7, 15, tzinfo=timezone.utc), mods)  # -> module jour 2
```

## Déployer (Modal)

```python
import modal

app = modal.App("whatsapp-drip_programme")
image = modal.Image.debian_slim().pip_install("httpx", "pyyaml", "python-dotenv")

@app.function(image=image, secrets=[modal.Secret.from_name("unipile")], schedule=modal.Cron("0 8 * * *"))
def daily():
    from scripts.whatsapp.drip_programme.run import run
    from lib import unipile_helpers as u
    run(u.load_config("scripts/whatsapp/drip_programme/config.example.yaml"))
```

Note : le journal d'idempotence (`state_path`) est local au conteneur. Pour un cron
Modal, pointer `state_path` vers un volume persistant (ou remplacer par votre DB) afin
de conserver l'état entre exécutions.
