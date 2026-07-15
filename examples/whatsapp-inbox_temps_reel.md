# Inbox WhatsApp temps réel - log de notifications (exemple fictif)

_Sortie illustrative de `notify()` : chaque ligne est un message entrant poussé vers Slack/CRM. Les messages sortants (les vôtres) n'apparaissent pas._

```
NOTIF ENTRANT: {"chat_id": "c-8821", "message_id": "m-1", "sender_name": "Camille Lefevre", "sender_id": "33600000001@s.whatsapp.net", "text": "Bonjour, vous êtes ouverts samedi ?"}
NOTIF ENTRANT: {"chat_id": "c-9042", "message_id": "m-2", "sender_name": "Thomas Mercier", "sender_id": "33600000002@s.whatsapp.net", "text": "Ma commande #1042 est-elle partie ?"}
NOTIF ENTRANT: {"chat_id": "c-7710", "message_id": "m-3", "sender_name": "Sofia Nguyen", "sender_id": "33600000003@s.whatsapp.net", "text": "Merci pour le devis, je reviens vers vous."}
```

Un message envoyé depuis votre propre compte (présent dans `UNIPILE_OWN_PROVIDER_IDS`) est ignoré : action `ignore`, aucune notification.
