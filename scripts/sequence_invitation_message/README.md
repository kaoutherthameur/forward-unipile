# 🔵 sequence_invitation_message (B2)

Séquence stateful : invite la cible → attend l'acceptation (détectée au degré de connexion)
→ envoie le 1er message. **Écriture** : simulé par défaut (`UNIPILE_DRY_RUN=1`).

- **Cadence** : récurrent (cron quotidien - chaque run fait avancer chaque cible d'une étape).
- **État** : fichier JSON local (`state.local.json`, gitignoré). Pas de DB (template).
- **Endpoints** : `GET /users/{id}` (degré), `POST /users/invite`, `POST /chats`.

## Lancer (simulé)

```bash
python scripts/sequence_invitation_message/run.py --config scripts/sequence_invitation_message/config.example.yaml
```

Jour 1 : invite. Jours suivants : si accepté → message. Sinon → wait.

## Déployer (Modal, cron quotidien)

Monte un volume Modal pour persister `state.local.json` entre les runs, ou remplace
`load_state`/`save_state` par ta base. Garde-fous (cap, fenêtre, jitter) déjà en place.
