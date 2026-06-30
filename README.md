# forward-unipile

> Kit de cas d'usage de l'**API LinkedIn via [Unipile](https://www.unipile.com/)** — par [Forward](https://www.forward-ai.fr).

Tout ce que l'API LinkedIn d'Unipile permet, sous **deux formes de ressources** :

- 🟢 **Skills MCP** (`.claude/skills/`) — à lancer **depuis Claude** avec le MCP Unipile connecté. Pour les usages **one-shot / ponctuels** (construire une liste, enrichir un CSV, sortir les engageurs d'un post).
- 🔵 **Scripts workflow** (`scripts/`) — Python + API REST, **déployables (Modal cron/webhook)**. Pour les usages **récurrents / planifiés** (drip d'invitations, relances, veille, webhook temps réel).

Catalogue complet des 38 cas d'usage : [`USE-CASES.md`](USE-CASES.md). Setup MCP : [`CONNECTING-MCP.md`](CONNECTING-MCP.md).

## Bien démarrer

1. `pip install -r requirements.txt`
2. `cp .env.example .env` puis renseigner `UNIPILE_DSN`, `UNIPILE_API_KEY`, `UNIPILE_ACCOUNT_ID`.
3. **Skills** : configurer le MCP Unipile (`cp mcp.example.json` vers la config de ton client, voir `CONNECTING-MCP.md`).
4. **Scripts** : `python scripts/{cas}/run.py --config scripts/{cas}/config.example.yaml`.

## Les ressources de ce kit (38 cas d'usage couverts)

### Prospection & ciblage (Sales)
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `unipile-prospects-salesnav` | 🟢 | Liste de prospects depuis Sales Navigator (filtres avancés) → CSV |
| `unipile-prospects-classic` | 🟢 | Liste de prospects en compte gratuit/Classic → CSV |
| `unipile-entreprises-cibles` | 🟢 | Liste d'entreprises cibles (ABM) → CSV |
| `unipile-enrichir-liste` | 🟢 | Enrichir un CSV de profils (poste, entreprise, degré, email visible) |
| `unipile-engageurs-post` | 🟢 | Les gens qui ont liké/commenté un post → liste de leads |
| `social_listening` | 🔵 | Posts récents sur un mot-clé → repérer qui en parle |

### Outreach automatisé (Sales)
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `invitation_drip` | 🔵 | Drip quotidien d'invitations + note, garde-fous anti-ban |
| `sequence_invitation_message` | 🔵 | Séquence invitation → acceptation → 1er message (stateful) |
| `relance_j3` | 🔵 | Relance unique des prospects silencieux à J+3 (anti-collision) |
| `unipile-inmail` | 🟢 | InMail vers un profil hors réseau (Sales Nav) |
| `nettoyer_invitations` | 🔵 | Retirer les invitations en attente > N jours (libère le quota) |
| `auto_accept_invitations` | 🔵 | Auto-accepter les invitations reçues + message de bienvenue |

### Recrutement (Talent)
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `unipile-sourcing-candidats` | 🟢 | Shortlist de candidats (skills, séniorité) via Recruiter/Sales Nav |
| `entreprises_qui_recrutent` | 🔵 | Scan des offres → entreprises qui recrutent un poste cible |
| `approche_candidats` | 🔵 | Approche candidats (invitation + note ou InMail Recruiter) |
| `unipile-publier-offre` | 🟢 | Créer / publier / clôturer une offre d'emploi LinkedIn |
| `pipeline_offre` | 🔵 | Candidats d'une offre + CV disponibles → CSV |

### Contenu & Engagement (Growth)
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `posts_performance` | 🔵 | Snapshot quotidien : impressions, réactions, visiteurs de profil, followers gagnés |
| `veille_concurrent` | 🔵 | Digest des posts récents d'un concurrent/influenceur + engagement |
| `unipile-activite-prospect` | 🟢 | Activité publique d'un prospect (commentaires/réactions) → accroches |
| `unipile-publier-post` | 🟢 | Publier un post LinkedIn par API |
| `unipile-commenter` | 🟢 | Commenter / répondre sur un post |
| `engagement_cible` | 🔵 | Liker/réagir à des posts ciblés (nurturing) |

### Réseau & Relations
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `profile_views` | 🔵 | Qui a visité votre profil (visiteurs identifiés) → leads entrants |
| `unipile-exporter-reseau` | 🟢 | Exporter tout votre réseau 1er degré → CSV |
| `unipile-audit-followers` | 🟢 | Lister abonnés & comptes suivis |
| `unipile-gerer-membre` | 🟢 | Suivre / ne plus suivre / bloquer un membre |
| `endorse_nurturing` | 🔵 | Recommander des compétences (nurturing) |
| `warm_touch` | 🔵 | Déclencher une visite de profil visible (touche douce) |

### Inbox & Messaging
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `unipile-inbox` | 🟢 | Lire vos conversations LinkedIn (multi-comptes) depuis Claude |
| `webhook_reponses` | 🔵 | Webhook temps réel : nouveau message → notif Slack/IA |
| `unipile-envoyer-piece-jointe` | 🟢 | Envoyer un DM avec pièce jointe (image, fichier, note vocale) |
| `unipile-gerer-messages` | 🟢 | Réagir / éditer / transférer / supprimer un message |
| `message_lifecycle` | 🔵 | Suivi temps réel (lu, livré, réaction) |

### CRM & Automatisation (Ops)
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `sync_connexions_crm` | 🔵 | Nouvelle connexion (webhook) → fiche CRM |
| `enrichissement_crm` | 🔵 | Profil + entreprise → fiche CRM enrichie |
| `unipile-connecter-comptes` | 🟢 | Connecter & gérer les comptes LinkedIn (hosted auth, checkpoints) |
| `monitoring_comptes` | 🔵 | Alerte si un compte se déconnecte / checkpoint |
| `unipile-raw-voyager` | 🟢 | Proxy d'un endpoint Voyager interne (avancé) |

> Détail et classification dans [`USE-CASES.md`](USE-CASES.md). Les scripts CRM (`sync_connexions_crm`, `enrichissement_crm`) exposent un stub `to_crm()` générique à câbler à votre CRM.

## Sécurité & anti-ban

- Secrets via `.env` (jamais commit).
- Les écritures (invitation, DM) tournent en **`DRY_RUN` par défaut** (`UNIPILE_DRY_RUN=1`) : rien n'est envoyé tant que tu ne passes pas `UNIPILE_DRY_RUN=0`.
- Garde-fous intégrés (`lib/unipile_helpers.py`) : plafond quotidien (`UNIPILE_DAILY_CAP`), fenêtre horaire locale du prospect, espacement aléatoire. Respecte les [limites LinkedIn](https://developer.unipile.com/docs/provider-limits-and-restrictions) — dépasser = risque de restriction du compte.

## Aller plus loin

- Doc Unipile : https://developer.unipile.com
- Cas d'usage Forward : https://www.forward-ai.fr/cas-d-usage *(page Unipile à venir)*

MIT.
