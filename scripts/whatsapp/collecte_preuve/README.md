# 🔵 whatsapp/collecte_preuve (E5)

Rappelle chaque jour à chaque coaché son exercice et lui demande une preuve (photo ou
note vocale). Le message est composé par la fonction pure `build_proof_request()`
(prénom + exercice + type de preuve demandé).

Écriture simulée par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron, une fois par jour).
- **Endpoints** : `POST /chats/{id}/messages` (envoi du rappel + demande de preuve).
- **Garde-fous** : envoi `is_write=True` + `UNIPILE_DRY_RUN` par défaut. Plafond quotidien (`u.daily_cap()`), fenêtre locale (`u.in_send_window()`), jitter (`u.sleep_jitter()`).

## Réception de la preuve (photo/audio)

Ce script ne gère **que la relance sortante**. Quand le coaché répond avec une photo
ou une note vocale, le média arrive via **webhook** `message_received` (payload avec
`attachment: {type: "image"/"audio", url}`). Pour capter et traiter cette pièce
jointe, brancher :

- **E2 `whatsapp/accountability`** (webhook) : logguer la progression à réception.
- **A1 / inbox temps réel** (webhook) : capter tout message entrant, dont les médias.
- **E6 `whatsapp/transcription_vocale`** (webhook) : si la preuve est une note vocale, la transcrire et la résumer pour le coach.

## Lancer (simulé)

```bash
python scripts/whatsapp/collecte_preuve/run.py --config scripts/whatsapp/collecte_preuve/config.example.yaml
```

Fonction pure testable hors-ligne :

```python
from scripts.whatsapp.collecte_preuve.run import build_proof_request
build_proof_request({"prenom": "Camille", "exercice_du_jour": "10 pompes"}, "photo")
```

## Déployer (Modal)

```python
import modal

app = modal.App("whatsapp-collecte_preuve")
image = modal.Image.debian_slim().pip_install("httpx", "pyyaml", "python-dotenv")

@app.function(image=image, secrets=[modal.Secret.from_name("unipile")], schedule=modal.Cron("0 9 * * *"))
def daily():
    from scripts.whatsapp.collecte_preuve.run import run
    from lib import unipile_helpers as u
    run(u.load_config("scripts/whatsapp/collecte_preuve/config.example.yaml"))
```

Compte perso : garder le volume bas, envois OPT-IN uniquement. Passer
`UNIPILE_DRY_RUN=0` seulement une fois la liste vérifiée.
