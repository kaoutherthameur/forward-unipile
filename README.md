# forward-unipile

> Kit de cas d'usage de l'API LinkedIn via [Unipile](https://www.unipile.com/) — par [Forward](https://www.forward-ai.fr).

Deux formes de ressources :

- 🟢 **Skills MCP** (`.claude/skills/`) — à lancer **depuis Claude** avec le MCP Unipile, pour les usages **one-shot** (construire une liste, enrichir un CSV, sortir les engageurs d'un post).
- 🔵 **Scripts workflow** (`scripts/`) — Python + API REST, **déployables (Modal cron/webhook)**, pour les usages **récurrents** (drip d'invitations, relances, veille, webhook temps réel).

> README en cours de construction (finalisé au dernier slice). Voir `USE-CASES.md` pour le catalogue complet des 38 cas d'usage et `CONNECTING-MCP.md` pour le setup MCP.

## Bien démarrer

1. `pip install -r requirements.txt`
2. `cp .env.example .env` puis renseigner `UNIPILE_DSN`, `UNIPILE_API_KEY`, `UNIPILE_ACCOUNT_ID`.
3. Skills : configurer le MCP Unipile (`cp mcp.example.json ...`, voir `CONNECTING-MCP.md`).
4. Scripts : `python scripts/{cas}/run.py --config scripts/{cas}/config.example.yaml`.

## Sécurité & anti-ban

- Secrets via `.env` (jamais commit).
- Les écritures (invitation, DM) tournent en **`DRY_RUN` par défaut** (`UNIPILE_DRY_RUN=1`).
- Garde-fous intégrés : plafond quotidien, fenêtre horaire locale, espacement aléatoire. Respecte les [limites LinkedIn](https://developer.unipile.com/docs/provider-limits-and-restrictions).
