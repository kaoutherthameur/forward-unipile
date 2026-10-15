# Relance de devis WhatsApp - sortie fictive (exemple illustratif)

_Exécution simulée (`UNIPILE_DRY_RUN=1`) le 2026-07-15 à 08h00 (heure FR)._

## Relances détectées comme dues

| chat_id | palier | clé d'idempotence | statut |
|---|---|---|---|
| CHAT_DEMO_DEVIS_1 | J+4 | `CHAT_DEMO_DEVIS_1\|J+4` | envoyé (simulé) |
| CHAT_DEMO_DEVIS_2 | - | - | aucun palier atteint (envoyé hier) |

## Message simulé envoyé

> Bonjour Thomas, avez-vous pu regarder le devis ? Je reste dispo si une ligne mérite d'être ajustée.

## Journal console (extrait)

```
[DRY_RUN] POST chats/CHAT_DEMO_DEVIS_1/messages json={'text': 'Bonjour Thomas, avez-vous pu regarder le devis ? Je reste dispo si une ligne mérite d\'être ajustée.'}
relance J+4 -> CHAT_DEMO_DEVIS_1 (DRY_RUN)
Terminé. 1 relance(s) simulée(s).
```

Le palier J+8 ne partira que dans 4 jours, et une seule fois grâce à la clé `CHAT_DEMO_DEVIS_1|J+8`.
