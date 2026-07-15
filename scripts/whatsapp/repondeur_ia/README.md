# 🔵 whatsapp/repondeur_ia (A2)

Répond en 1er niveau aux messages WhatsApp entrants via `answer_faq()` (déterministe
sur mots-clés : horaires, prix, dispo, adresse). Si aucun motif ne correspond,
`answer_faq()` renvoie `None` et le message est escaladé à un humain via `escalate()`.

Écriture simulée par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (webhook `message_received`).
- **Endpoints** : `POST /chats/{id}/messages` (envoi de la réponse FAQ).
- **Garde-fous** : envoi `is_write=True` + `UNIPILE_DRY_RUN` par défaut. Filtrage des messages sortants via `UNIPILE_OWN_PROVIDER_IDS`. Réponse uniquement sur motif reconnu, sinon escalade humaine (pas d'envoi automatique dans le doute).

## Lancer (simulé)

Fonctions pures testables hors-ligne :

```python
from scripts.whatsapp.repondeur_ia.app import answer_faq, process_event
answer_faq("Quels sont vos horaires ?")   # -> réponse horaires
answer_faq("Vous reprenez les retours ?")  # -> None (escalade)
```

## Déployer (Modal)

```bash
modal deploy scripts/whatsapp/repondeur_ia/app.py
```

Enregistrer l'URL comme webhook `message_received` côté Unipile (`POST /webhooks`).
Remplacer `answer_faq()` par un appel LLM si besoin (en gardant l'escalade humaine
sur faible confiance). Compte perso : rester conversationnel et déclenché par message.
