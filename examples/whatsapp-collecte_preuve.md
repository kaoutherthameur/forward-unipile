# Collecte de preuve WhatsApp - demande + réception (exemple fictif)

_Illustratif. La demande sortante est simulée (DRY_RUN). La réception de la preuve_
_arrive via webhook (voir E2 / A1 / E6), montrée ici pour le contexte._

## Demande sortante (ce script, DRY_RUN)

**-> Camille** : Salut Camille ! L'exercice du jour : 10 pompes + 5 min de respiration. Envoie-moi une photo pour prouver que c'est fait.
**-> Thomas** : Salut Thomas ! L'exercice du jour : lire 10 pages de ton livre. Envoie-moi une note vocale de 30 secondes pour me raconter.

```
demande de preuve DRY_RUN -> Camille : Salut Camille ! L'exercice du jour : 10 pompes + 5 min de respiration. Envoie-moi une photo pour prouver que c'est fait.
demande de preuve DRY_RUN -> Thomas : Salut Thomas ! L'exercice du jour : lire 10 pages de ton livre. Envoie-moi une note vocale de 30 secondes pour me raconter.
Terminé. 2 demande(s) simulée(s).
```

## Réception de la preuve (via webhook, illustratif)

Quand Camille répond avec une photo, le média arrive dans un payload webhook :

```json
{
  "event": "message_received",
  "chat_id": "c-3001",
  "sender": {"attendee_provider_id": "3361234...", "attendee_name": "Camille"},
  "attachment": {"type": "image", "url": "https://exemple.test/preuve-camille.jpg"}
}
```

Ce payload est capté par E2 (accountability) ou A1 (inbox temps réel). Si la preuve
est une note vocale, E6 (transcription_vocale) la transcrit et la résume.
