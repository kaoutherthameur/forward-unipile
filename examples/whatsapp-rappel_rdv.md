# Rappels de RDV WhatsApp - sortie fictive (exemple illustratif)

_Exécution simulée (`UNIPILE_DRY_RUN=1`) le 2026-07-15 à 15h30 (heure FR)._

## Rappels détectés comme dus

| chat_id | étape | clé d'idempotence | statut |
|---|---|---|---|
| CHAT_DEMO_RDV_1 | J-1 | `CHAT_DEMO_RDV_1\|J-1\|2026-07-15` | ignoré (déjà envoyé) |
| CHAT_DEMO_RDV_2 | H-2 | `CHAT_DEMO_RDV_2\|H-2\|2026-07-15` | envoyé (simulé) |

## Message simulé envoyé

> Bonjour Léa, on se retrouve dans 2h (17h30). À tout de suite !

## Journal console (extrait)

```
skip (déjà envoyé) : CHAT_DEMO_RDV_1
[DRY_RUN] POST chats/CHAT_DEMO_RDV_2/messages json={'text': 'Bonjour Léa, on se retrouve dans 2h (17h30). À tout de suite !'}
rappel H-2 -> CHAT_DEMO_RDV_2 (DRY_RUN)
Terminé. 1 rappel(s) simulé(s).
```

Le rappel J-1 du premier RDV n'est pas réémis : sa clé figure déjà dans `already_sent`.
