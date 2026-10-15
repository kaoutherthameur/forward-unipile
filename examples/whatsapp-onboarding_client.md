# Onboarding client WhatsApp - sortie fictive (exemple illustratif)

_Exécution simulée (`UNIPILE_DRY_RUN=1`) le 2026-07-15 à 07h30 (heure FR)._

## Étapes détectées comme dues

| client | chat_id | étape du jour | clé d'idempotence | statut |
|---|---|---|---|---|
| CLIENT_DEMO_1 | CHAT_DEMO_ONB_1 | J0 | `CLIENT_DEMO_1\|J0` | envoyé (simulé) |
| CLIENT_DEMO_2 | CHAT_DEMO_ONB_2 | J+2 | `CLIENT_DEMO_2\|J+2` | envoyé (simulé) |

## Séquence complète (les 3 messages, client CLIENT_DEMO_1)

> **J0** - Bienvenue Julie ! Ravi de vous compter parmi nous. Je reste joignable ici si besoin.

> **J+2** - Bonjour Julie, un petit conseil pour bien démarrer : commencez par configurer votre espace, ça prend 5 minutes.

> **J+7** - Bonjour Julie, une semaine déjà ! Tout se passe bien ? Dites-moi si je peux vous aider sur un point.

## Journal console (extrait)

```
[DRY_RUN] POST chats/CHAT_DEMO_ONB_1/messages json={'text': 'Bienvenue Julie ! ...'}
onboarding J0 -> CHAT_DEMO_ONB_1 (DRY_RUN)
[DRY_RUN] POST chats/CHAT_DEMO_ONB_2/messages json={'text': 'Bonjour Marc, un conseil pour bien démarrer : ...'}
onboarding J+2 -> CHAT_DEMO_ONB_2 (DRY_RUN)
Terminé. 2 message(s) simulé(s).
```

La bienvenue J0 de CLIENT_DEMO_2 n'est pas réémise : sa clé `CLIENT_DEMO_2|J0` est déjà dans `already_sent`.
