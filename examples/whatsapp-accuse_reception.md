# Accusé de réception hors heures - log (exemple fictif)

_Sortie illustrative. Fenêtre d'ouverture : 07:30-19:30 (heure FR). Les envois marqués DRY_RUN sont simulés (aucun envoi réel)._

```
# Message reçu à 22h41 FR (hors fenêtre) -> accusé envoyé
ACCUSE DRY_RUN -> chat c-8821 : Bien reçu, merci pour votre message. On revient vers vous sous 2h ouvrées.

# Message reçu à 06h12 FR (hors fenêtre) -> accusé envoyé
ACCUSE DRY_RUN -> chat c-9042 : Bien reçu, merci pour votre message. On revient vers vous sous 2h ouvrées.

# Message reçu à 14h05 FR (dans la fenêtre) -> aucun accusé (action ignore, un humain répond)
```
