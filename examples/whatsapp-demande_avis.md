# Demande d'avis WhatsApp - sortie fictive (exemple illustratif)

_Exécution simulée (`UNIPILE_DRY_RUN=1`) le 2026-07-15 à 08h00 (heure FR)._

## Prestations détectées comme éligibles

| chat_id | prestation | clé d'idempotence | statut |
|---|---|---|---|
| CHAT_DEMO_AVIS_1 | il y a 3 jours | `CHAT_DEMO_AVIS_1\|avis` | envoyé (simulé) |
| CHAT_DEMO_AVIS_2 | hier | - | pas encore éligible (délai 3 jours) |

## Message simulé envoyé (lien injecté)

> Bonjour Nadia, merci pour votre confiance ! Si vous avez 30 secondes, un petit avis m'aiderait beaucoup : https://g.page/r/exemple-avis-fictif/review

## Journal console (extrait)

```
[DRY_RUN] POST chats/CHAT_DEMO_AVIS_1/messages json={'text': 'Bonjour Nadia, merci pour votre confiance ! ... https://g.page/r/exemple-avis-fictif/review'}
demande d'avis -> CHAT_DEMO_AVIS_1 (DRY_RUN)
Terminé. 1 demande(s) simulée(s).
```

Relancé demain, le script ne réémettra pas cette demande : la clé `CHAT_DEMO_AVIS_1|avis` sera dans `already_sent`.
