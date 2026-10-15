---
name: unipile-envoyer-piece-jointe
description: Use when you want to send a LinkedIn DM with an attachment (image, file, voice note), one-shot. Recipient + file -> message sent.
---
# Envoyer une pièce jointe en DM

## Objectif & quand
One-shot : envoyer un message LinkedIn avec une pièce jointe (image, vidéo, fichier, note vocale) - ex. envoyer une ressource à un prospect.

## Prérequis
- Compte LinkedIn connecté à Unipile (Classic). MCP Unipile configuré.

## Config (`config.example.yaml`)
| Champ | Rôle |
|---|---|
| `recipient` | slug/URL (nouveau chat) ou `chat_id` (chat existant) |
| `text` | message d'accompagnement |
| `attachment_path` | chemin du fichier à joindre |

## Procédure (via MCP)
1. Résoudre le destinataire (`provider_id` via `GET /users/{id}`) ou utiliser `chat_id`.
2. Envoyer le message avec la pièce jointe (`POST /chats/{id}/messages` ou `POST /chats`).

## Si le MCP ne fait pas l'action
```python
from lib import unipile_helpers as u
# pièce jointe : multipart selon le client ; en REST, POST /chats/{id}/messages avec le fichier
u.post(f"chats/{chat_id}/messages", json={"text": "Voici la ressource"}, is_write=True)
```

## Livrable
Message + pièce jointe envoyés (ou simulé en `DRY_RUN`).

## Limites & anti-ban
Écriture. Types supportés : image, vidéo, fichier, note vocale.

## Exemple
Snippet ci-dessus (action one-shot).
