# Tri des demandes WhatsApp - demandes classées (exemple fictif)

_Sortie illustrative de `classify()` + `route_to()` sur un lot de messages entrants._

| Expéditeur | Message | Catégorie | Routé vers |
|---|---|---|---|
| Camille Lefevre | "Mon colis #1042 n'est toujours pas arrivé" | commande | outil commandes |
| Thomas Mercier | "L'appareil est tombé en panne au bout de 3 jours" | sav | file support |
| Sofia Nguyen | "Je voudrais réserver une table pour 4 samedi soir" | reservation | agenda |
| Julien Carre | "Vous avez GAGNÉ un iPhone, cliquez ici bit.ly/xxx" | spam | corbeille |
| Léa Fontaine | "Bonjour, juste pour vous remercier :)" | autre | file support (défaut) |

```
ROUTAGE [commande]: {"chat_id": "c-8821", "sender_name": "Camille Lefevre", "text": "Mon colis #1042 n'est toujours pas arrivé"}
ROUTAGE [sav]: {"chat_id": "c-9042", "sender_name": "Thomas Mercier", "text": "L'appareil est tombé en panne au bout de 3 jours"}
ROUTAGE [reservation]: {"chat_id": "c-7710", "sender_name": "Sofia Nguyen", "text": "Je voudrais réserver une table pour 4 samedi soir"}
ROUTAGE [spam]: {"chat_id": "c-6120", "sender_name": "Julien Carre", "text": "Vous avez GAGNÉ un iPhone, cliquez ici bit.ly/xxx"}
```
