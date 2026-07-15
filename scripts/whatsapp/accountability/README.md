# 🔵 whatsapp/accountability (E2)

Quand un coaché répond son avancement sur WhatsApp, le webhook classe le message via
`classify_progress()` (done / blocked / unclear), compose une relance ou un
encouragement via `coach_reply()`, historise via `log_progress()`, puis renvoie la
réponse dans le fil.

Écriture simulée par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (webhook `message_received`).
- **Endpoints** : `POST /chats/{id}/messages` (envoi de la relance/encouragement).
- **Garde-fous** : envoi `is_write=True` + `UNIPILE_DRY_RUN` par défaut. Filtrage des messages sortants via `UNIPILE_OWN_PROVIDER_IDS`. `coach_reply()` est un stub déterministe (à câbler sur un LLM). `log_progress()` est un stub (à câbler sur un Sheet/CRM).

## Lancer (simulé)

Fonctions pures testables hors-ligne :

```python
from scripts.whatsapp.accountability.app import classify_progress, coach_reply, process_event
classify_progress("C'est fait, j'ai publié !")   # -> "done"
coach_reply("j'ai pas eu le temps, bloqué")        # -> encouragement + petit pas
```

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/accountability/app.py
```

Enregistrer l'URL comme webhook `message_received` côté Unipile (`POST /webhooks`).
Remplacer `coach_reply()` par un appel LLM (en gardant un ton coach, encourageant,
jamais culpabilisant) et `log_progress()` par une écriture dans votre outil de suivi.
Compte perso : rester conversationnel et déclenché par le message du coaché.
