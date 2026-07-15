# Relance de panier WhatsApp - sortie fictive (exemple illustratif)

_Exécution simulée (`UNIPILE_DRY_RUN=1`) le 2026-07-15 à 08h00 (heure FR)._

## Événements évalués

| chat_id | event_id | abandon | clé d'idempotence | statut |
|---|---|---|---|---|
| CHAT_DEMO_PANIER_1 | PANIER_2026_07_15_A | il y a ~4h | `CHAT_DEMO_PANIER_1\|PANIER_2026_07_15_A` | envoyé (simulé) |
| CHAT_DEMO_PANIER_2 | RESA_2026_07_15_B | il y a ~1h | - | pas encore éligible (délai 4h) |

## Message simulé envoyé

> Bonjour Inès, votre panier vous attend toujours ! Un doute sur un article ? Je réponds ici avec plaisir.

## Journal console (extrait)

```
[DRY_RUN] POST chats/CHAT_DEMO_PANIER_1/messages json={'text': 'Bonjour Inès, votre panier vous attend toujours ! ...'}
relance panier -> CHAT_DEMO_PANIER_1 (DRY_RUN)
Terminé. 1 rappel(s) simulé(s).
```

Un rappel **unique** par panier : au prochain passage, la clé `CHAT_DEMO_PANIER_1|PANIER_2026_07_15_A` sera dans `already_sent` et rien ne repartira.
