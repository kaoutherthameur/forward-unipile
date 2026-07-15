# Répondeur IA WhatsApp de 1er niveau - échanges (exemple fictif)

_Échanges illustratifs. Les réponses marquées DRY_RUN sont simulées (aucun envoi réel)._

**Camille** : Bonjour, vous êtes ouverts le samedi ?
**Répondeur (FAQ)** : Nous sommes ouverts du lundi au samedi, de 9h à 19h. Fermé le dimanche.

**Thomas** : C'est combien la formule découverte ?
**Répondeur (FAQ)** : Nos tarifs démarrent à 29 EUR. Dites-moi le produit qui vous intéresse et je vous précise le prix exact.

**Sofia** : Le modèle bleu est encore dispo ?
**Répondeur (FAQ)** : Je vérifie la disponibilité et je vous confirme sous quelques minutes.

**Julien** : J'ai un souci avec ma facture du mois dernier, il y a une erreur.
**Répondeur** : _(aucun motif reconnu -> escalade humaine)_

```
REPONSE FAQ DRY_RUN -> chat c-8821 : Nous sommes ouverts du lundi au samedi, de 9h à 19h. Fermé le dimanche.
REPONSE FAQ DRY_RUN -> chat c-9042 : Nos tarifs démarrent à 29 EUR. Dites-moi le produit qui vous intéresse et je vous précise le prix exact.
REPONSE FAQ DRY_RUN -> chat c-7710 : Je vérifie la disponibilité et je vous confirme sous quelques minutes.
ESCALADE HUMAINE: {"chat_id": "c-6120", "sender_name": "Julien Carre", "text": "J'ai un souci avec ma facture du mois dernier, il y a une erreur."}
```
