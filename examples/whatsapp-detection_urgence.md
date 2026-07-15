# Détection d'urgence WhatsApp - alertes (exemple fictif)

_Sortie illustrative de `alert()`. Seuls les messages contenant un signal de churn/urgence déclenchent une alerte ; les autres sont ignorés._

```
ALERTE URGENCE: {"chat_id": "c-8821", "sender_name": "Camille Lefevre", "keywords": ["annuler", "remboursement"], "text": "Je veux annuler mon abonnement et être remboursée, c'est inadmissible."}
ALERTE URGENCE: {"chat_id": "c-9042", "sender_name": "Thomas Mercier", "keywords": ["urgent", "déçu"], "text": "C'est urgent, je suis très déçu du service, personne ne me répond."}
ALERTE URGENCE: {"chat_id": "c-7710", "sender_name": "Sofia Nguyen", "keywords": ["résilier"], "text": "Comment je fais pour résilier ? Ça ne me convient plus."}
```

Messages ignorés (aucun mot-clé) : "Merci pour votre aide !", "Vous êtes ouverts demain ?".
