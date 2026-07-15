# Tâches auto depuis WhatsApp - messages vers tâches (exemple fictif)

_Sortie illustrative de `create_task()`. Chaque message entrant est évalué par `is_actionable()` ; seuls ceux qui portent une intention d'action déclenchent une tâche. Vos messages sortants sont ignorés._

## Messages entrants et décision

| Message reçu | Expéditeur | Décision |
|---|---|---|
| "Tu peux m'envoyer le devis du salon stp ?" | Camille Lefevre | create_task |
| "Il faudrait relancer le fournisseur avant vendredi." | Thomas Mercier | create_task |
| "N'oublie pas de réserver la salle pour jeudi." | Sofia Nguyen | create_task |
| "Super, merci beaucoup !" | Camille Lefevre | ignore (pas d'action) |
| "Je t'ai envoyé le fichier." (message sortant) | Vous | ignore (sortant) |

## Tâches créées (log `create_task`)

```
NOUVELLE TÂCHE: {"chat_id": "c-8821", "message_id": "m-11", "title": "Tu peux m'envoyer le devis du salon stp ?", "sender_name": "Camille Lefevre", "sender_id": "33600000001@s.whatsapp.net"}
NOUVELLE TÂCHE: {"chat_id": "c-9042", "message_id": "m-12", "title": "Il faudrait relancer le fournisseur avant vendredi.", "sender_name": "Thomas Mercier", "sender_id": "33600000002@s.whatsapp.net"}
NOUVELLE TÂCHE: {"chat_id": "c-7710", "message_id": "m-13", "title": "N'oublie pas de réserver la salle pour jeudi.", "sender_name": "Sofia Nguyen", "sender_id": "33600000003@s.whatsapp.net"}
```

Le titre reprend le message brut : à raffiner dans `create_task()` (résumé, échéance, assignation) selon l'outil cible.
