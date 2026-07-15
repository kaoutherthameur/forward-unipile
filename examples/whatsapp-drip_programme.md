# Drip programme WhatsApp "Décollage 5 jours" - modules (exemple fictif)

_Programme illustratif. Les envois marqués DRY_RUN sont simulés (aucun envoi réel)._

Le module délivré dépend de la date de démarrage de chaque coaché :
- **Camille** a démarré aujourd'hui -> reçoit le **Jour 1**.
- **Thomas** a démarré il y a 4 jours -> reçoit le **Jour 5**.

**-> Camille (Jour 1)**
> Jour 1 - Clarifier ta cible
>
> Écris en une phrase la personne que tu veux aider. Réponds-moi avec ta phrase.

**-> Thomas (Jour 5)**
> Jour 5 - Passe à l'action
>
> Envoie tes 5 messages aujourd'hui. Dis-moi quand c'est parti.

```
module J1 DRY_RUN -> Camille : Jour 1 - Clarifier ta cible
module J5 DRY_RUN -> Thomas : Jour 5 - Passe à l'action
Terminé. 2 module(s) simulé(s).
```

_Idempotence : si le cron repasse dans la journée, les clés `c-3001:1` et `c-3002:5`_
_sont déjà dans le journal -> aucun renvoi._
