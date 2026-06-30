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

## Les ressources de ce kit

### Prospection & ciblage (Sales)
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `unipile-prospects-salesnav` | 🟢 | Liste de prospects depuis Sales Navigator (filtres avancés) → CSV |
| `unipile-enrichir-liste` | 🟢 | Enrichir un CSV de profils (poste, entreprise, degré, email visible) |
| `unipile-engageurs-post` | 🟢 | Les gens qui ont liké/commenté un post → liste de leads |
| `invitation_drip` | 🔵 | Drip quotidien d'invitations + note, garde-fous anti-ban |
| `relance_j3` | 🔵 | Relance unique des prospects silencieux à J+3 (anti-collision) |

### Recrutement (Talent)
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `unipile-sourcing-candidats` | 🟢 | Shortlist de candidats (skills, séniorité) via Recruiter/Sales Nav |
| `entreprises_qui_recrutent` | 🔵 | Scan des offres → entreprises qui recrutent un poste cible |

### Contenu & Growth
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `posts_performance` | 🔵 | Snapshot quotidien : impressions, réactions, visiteurs de profil, followers gagnés |
| `veille_concurrent` | 🔵 | Digest des posts récents d'un concurrent/influenceur + engagement |

### Ops & temps réel
| Ressource | Type | Ce que ça fait |
|---|---|---|
| `webhook_reponses` | 🔵 | Webhook temps réel : nouveau message LinkedIn → notif Slack/IA |

> 28 autres cas d'usage documentés en roadmap dans [`USE-CASES.md`](USE-CASES.md).

## Sécurité & anti-ban

- Secrets via `.env` (jamais commit).
- Les écritures (invitation, DM) tournent en **`DRY_RUN` par défaut** (`UNIPILE_DRY_RUN=1`) : rien n'est envoyé tant que tu ne passes pas `UNIPILE_DRY_RUN=0`.
- Garde-fous intégrés (`lib/unipile_helpers.py`) : plafond quotidien (`UNIPILE_DAILY_CAP`), fenêtre horaire locale du prospect, espacement aléatoire. Respecte les [limites LinkedIn](https://developer.unipile.com/docs/provider-limits-and-restrictions) — dépasser = risque de restriction du compte.

## Aller plus loin

- Doc Unipile : https://developer.unipile.com
- Cas d'usage Forward : https://www.forward-ai.fr/cas-d-usage *(page Unipile à venir)*

MIT.
