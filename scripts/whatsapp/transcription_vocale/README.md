# 🔵 whatsapp/transcription_vocale (E6)

Quand un coaché envoie une **note vocale** sur WhatsApp, le webhook la détecte
(`extract_audio()` repère un `attachment` de type `audio`), la transcrit
(`transcribe()`, stub STT), la résume (`summarize()`, stub LLM), puis livre le résumé
au coach (`deliver_to_coach()`, stub).

Écriture simulée par défaut (`UNIPILE_DRY_RUN=1`). Ici pas d'envoi WhatsApp : la
livraison va vers le coach (Slack/CRM/note), pas vers le coaché.

- **Cadence** : récurrent (webhook `message_received`).
- **Endpoints** : réception du payload webhook (`attachment: {type: "audio", url}`). Le téléchargement de l'audio se fait via l'`url` fournie.
- **Garde-fous** : filtrage des messages sortants via `UNIPILE_OWN_PROVIDER_IDS`. Traitement déclenché uniquement sur une pièce jointe audio (sinon `ignore`). `transcribe()`, `summarize()` et `deliver_to_coach()` sont des stubs.

## Lancer (simulé)

Fonctions pures testables hors-ligne :

```python
from scripts.whatsapp.transcription_vocale.app import extract_audio, process_event
extract_audio({"attachment": {"type": "audio", "url": "https://exemple.test/v.ogg"}})  # -> url
process_event({"event": "message_received", "attachment": {"type": "audio", "url": "https://exemple.test/v.ogg"}}, set())
```

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/transcription_vocale/app.py
```

Enregistrer l'URL comme webhook `message_received` côté Unipile (`POST /webhooks`).
Remplacer `transcribe()` par un appel STT (Whisper, etc.) sur l'`url` de l'audio, et
`summarize()` par un appel LLM. Brancher `deliver_to_coach()` sur l'outil où le coach
prépare ses séances (Slack, CRM, note de coaching).
