# Accountability WhatsApp - échange coaché/coach (exemple fictif)

_Échange illustratif. Les relances marquées DRY_RUN sont simulées (aucun envoi réel)._

**Camille** : C'est fait ! J'ai bouclé mes 30 min de rédaction ce matin.
**Coach (IA)** : Bravo, ça c'est de la régularité ! Une fois posé, quelle est la prochaine petite action ?

**Thomas** : J'ai pas eu le temps, ça a été une grosse journée, je suis un peu bloqué.
**Coach (IA)** : Pas de souci, ça arrive. C'est quoi le plus petit pas que tu peux faire aujourd'hui, même 5 minutes ?

**Sofia** : Bof, mitigé.
**Coach (IA)** : Merci pour ton retour ! Dis-m'en un peu plus : tu as pu avancer ou quelque chose t'a bloqué ?

```
PROGRESS: {"chat_id": "c-3001", "sender_name": "Camille", "status": "done", "text": "C'est fait ! J'ai bouclé mes 30 min de rédaction ce matin."}
RELANCE DRY_RUN -> chat c-3001 : Bravo, ça c'est de la régularité ! Une fois posé, quelle est la prochaine petite action ?
PROGRESS: {"chat_id": "c-3002", "sender_name": "Thomas", "status": "blocked", "text": "J'ai pas eu le temps, ça a été une grosse journée, je suis un peu bloqué."}
RELANCE DRY_RUN -> chat c-3002 : Pas de souci, ça arrive. C'est quoi le plus petit pas que tu peux faire aujourd'hui, même 5 minutes ?
PROGRESS: {"chat_id": "c-3003", "sender_name": "Sofia", "status": "unclear", "text": "Bof, mitigé."}
RELANCE DRY_RUN -> chat c-3003 : Merci pour ton retour ! Dis-m'en un peu plus : tu as pu avancer ou quelque chose t'a bloqué ?
```
