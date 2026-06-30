# Forward Unipile x LinkedIn — Catalogue de cas d'usage

> Cadrage (2026-06-30). Recensement **exhaustif** des cas d'usage permis par l'API LinkedIn d'Unipile, pour le lead magnet `forward-unipile`, sur le modèle de `forward-linkup` (repo de skills Claude Code réutilisables : 1 skill = `SKILL.md` + `config.yaml` + `run.py`).
> Angle : **tout ce que l'API LinkedIn permet via Unipile**. Focus LinkedIn. WhatsApp = itération ultérieure.
> Instance 2 du projet Kit Outils (après l'instance 1 LinkUp).

## Sources

- **Doc officielle Unipile** : developer.unipile.com (89 endpoints, surface API LinkedIn complète)
- **`forward-graph`** : suivi des posts (sync posts, engagement, profile views, DM, webhooks)
- **Melvin** (`forward-tier1-analyst` / `shared/repos/hermes/melvin`) : agent outreach (invitation, DM, relances, séquences, garde-fous anti-ban)

## Légende

**Provenance** : ✅ prouvé en prod dans `forward-graph` · 🤝 prouvé en prod dans Melvin · 📘 doc Unipile (à valider en build)
**Prérequis LinkedIn** : Classic (gratuit/Premium) · Sales Nav · Recruiter
**Type** : Atomique (1 capacité API) · Composite (workflow multi-étapes)

---

## Famille A — Prospection & ciblage (Sales)

| # | Cas d'usage | Bénéfice | Endpoints | Prérequis | Type | Provenance |
|---|---|---|---|---|---|---|
| A1 | **Liste de prospects via Sales Navigator** | Liste ICP ciblée (séniorité, secteur, effectif, "a changé de poste") → CSV | `POST /linkedin/search` (sales_navigator, people) | Sales Nav | Composite | 📘 |
| A2 | **Liste de prospects via recherche Classic** | Même chose en compte gratuit, filtres plus simples | `POST /linkedin/search` (classic, people) | Classic | Composite | 📘 |
| A3 | **Liste d'entreprises cibles (ABM)** | Construire une liste de comptes (secteur, effectif, localisation) | `POST /linkedin/search` (companies) | Classic/Sales Nav | Composite | 📘 |
| A4 | **Capter les profils qui engagent un post** | Likers + commentateurs d'un post (le vôtre, un concurrent, un influenceur) = liste chaude | `GET /posts/{id}/reactions`, `/comments` | Classic | Composite | ✅ |
| A5 | **Social listening : recherche de posts par mot-clé** | Repérer qui parle d'un sujet → prospects à engager | `POST /linkedin/search` (posts) | Classic | Composite | 📘 |
| A6 | **Enrichir une liste de prospects** | URLs/slugs → profil complet (poste, entreprise, taille, degré, email pro si visible) | `GET /users/{id}`, `GET /linkedin/companies/{id}` | Classic | Composite | ✅📘 |

## Famille B — Outreach automatisé (Sales)

| # | Cas d'usage | Bénéfice | Endpoints | Prérequis | Type | Provenance |
|---|---|---|---|---|---|---|
| B1 | **Invitation automatique de votre cible** | Recherche → invitation + note personnalisée en masse (avec garde-fous) | `POST /linkedin/search` + `POST /users/invite` | Classic | Composite | 🤝📘 |
| B2 | **Séquence invitation → message** | Inviter → détecter acceptation → envoyer le 1er DM | `POST /users/invite`, webhook `new_relation`, `POST /chats` | Classic | Composite | 🤝 |
| B3 | **Relance automatique des sans-réponse (J+3)** | Détecter le silence et relancer une fois, fenêtre horaire respectée | `GET /chats/{id}/messages`, `POST /chats/{id}/messages` | Classic | Composite | 🤝 |
| B4 | **InMail aux profils hors réseau / Open Profiles** | Contacter sans être connecté (quota InMail) | `POST /chats` (inmail), `GET /linkedin/credits` | Sales Nav | Atomique | 📘 |
| B5 | **Nettoyer les invitations en attente** | Retirer (withdraw) les invitations > N jours pour libérer le quota hebdo | `GET /users/invitations/sent`, `DELETE /users/invite/{id}` | Classic | Composite | 📘 |
| B6 | **Auto-accepter les invitations reçues + bienvenue** | Accepter les invitations entrantes et envoyer un message de bienvenue | `GET /users/invitations/received`, `PATCH /users/invitations/{id}`, `POST /chats` | Classic | Composite | 📘 |

## Famille C — Recrutement (Talent)

| # | Cas d'usage | Bénéfice | Endpoints | Prérequis | Type | Provenance |
|---|---|---|---|---|---|---|
| C1 | **Sourcer des candidats** | Shortlist filtrée (skills, fonction, séniorité, secteur) | `POST /linkedin/search` (recruiter/sales_navigator, people) | Recruiter/Sales Nav | Composite | 📘 |
| C2 | **Détecter les entreprises qui recrutent un poste** | Signal (prospection "ils structurent" ou veille RH) depuis les offres | `POST /linkedin/search` (jobs) | Classic | Composite | 📘 |
| C3 | **Approche candidats automatisée** | Invitation + InMail Recruiter personnalisés | `POST /users/invite`, `POST /chats` (recruiter) | Recruiter | Composite | 📘🤝 |
| C4 | **Publier / gérer une offre d'emploi via API** | Créer, publier, modifier, clôturer une offre LinkedIn par API | `POST/PUT /linkedin/jobs`, `.../publish`, `.../close` | Recruiter | Atomique | 📘 |
| C5 | **Gérer la pipeline d'une offre** | Lister les candidats + télécharger les CV | `GET /linkedin/jobs/{id}/applicants`, `.../resume` | Recruiter | Composite | 📘 |

## Famille D — Contenu & Engagement (Growth)

| # | Cas d'usage | Bénéfice | Endpoints | Prérequis | Type | Provenance |
|---|---|---|---|---|---|---|
| D1 | **Publier un post LinkedIn par API** | Programmer/automatiser la publication de contenu | `POST /posts` | Classic | Atomique | 📘 |
| D2 | **Commenter / répondre automatiquement** | Commenter des posts ciblés, répondre aux commentaires de vos posts (avec mentions) | `POST /posts/{id}/comments` (+ `comment_id`, `mentions`) | Classic | Atomique | 📘 |
| D3 | **Liker / réagir à des posts ciblés** | Engagement de nurturing sur des comptes cibles | `POST /posts/{id}/reactions` | Classic | Atomique | 📘 |
| D4 | **Tableau de bord de performance de vos posts** | Par post : impressions, réactions, commentaires, reposts, visiteurs de profil & followers générés | `GET /posts/{id}` (+ analytics) | Classic | Composite | ✅ |
| D5 | **Veille de contenu concurrent / influenceur** | Digest périodique des posts d'un profil + leur engagement | `GET /users/{id}/posts` | Classic | Composite | ✅ |
| D6 | **Suivre l'activité publique d'un prospect** | Ses commentaires/réactions récents → angle d'accroche personnalisé | `GET /users/{id}/comments`, `/reactions` | Classic | Composite | 📘 |

## Famille E — Réseau & Relations

| # | Cas d'usage | Bénéfice | Endpoints | Prérequis | Type | Provenance |
|---|---|---|---|---|---|---|
| E1 | **Qui a visité mon profil → leads entrants** | Récupérer les visiteurs identifiés du profil pour les qualifier | `POST /linkedin` raw (Voyager `wvmpCards`) | Classic (Premium reco) | Composite | ✅ |
| E2 | **Exporter tout votre réseau** | Liste des connexions 1er degré → CSV (backup, analyse, CRM) | `GET /users/relations` | Classic | Atomique | 📘 |
| E3 | **Auditer followers & following** | Lister abonnés et comptes suivis | `GET /users/followers`, `/following` | Classic | Atomique | 📘 |
| E4 | **Suivre / ne plus suivre / bloquer un membre** | Gérer les abonnements et blocages par API | `POST /linkedin/members/{id}/action` | Classic | Atomique | 📘 |
| E5 | **Recommander des compétences (endorse)** | Nurturing relationnel automatisé sur des contacts cibles | `POST /linkedin/skills/{id}/endorse` | Classic | Atomique | 📘 |
| E6 | **"Warm touch" : visite de profil déclenchée** | Apparaître dans le "qui a vu votre profil" d'une cible (`notify=true`) | `GET /users/{id}` (`notify=true`) | Classic | Atomique | 📘 |

## Famille F — Inbox & Messaging

| # | Cas d'usage | Bénéfice | Endpoints | Prérequis | Type | Provenance |
|---|---|---|---|---|---|---|
| F1 | **Inbox LinkedIn unifiée multi-comptes** | Centraliser et lire toutes les conversations de l'équipe | `GET /chats`, `/chats/{id}/messages`, `/chat_attendees` | Classic | Composite | 📘 |
| F2 | **Réponse temps réel (webhook → notif / IA)** | Nouveau message → notif Slack instantanée et/ou réponse IA | webhook `message_received` | Classic | Composite | ✅🤝 |
| F3 | **Envoyer des pièces jointes en DM** | Image, vidéo, fichier, note vocale dans un message | `POST /chats/{id}/messages` (attachments) | Classic | Atomique | 📘 |
| F4 | **Agir sur les messages (réagir/éditer/transférer/supprimer)** | Gérer le contenu des conversations par API | `POST /messages/{id}/reactions`, `PUT/DELETE /messages/{id}`, `/forward` | Classic | Atomique | 📘 |
| F5 | **Suivre le cycle de vie des messages** | Accusés lu/livré, réactions sur vos messages via webhooks | webhooks `message_read`, `_delivered`, `_reaction` | Classic | Atomique | 📘 |

## Famille G — CRM & Automatisation (Ops)

| # | Cas d'usage | Bénéfice | Endpoints | Prérequis | Type | Provenance |
|---|---|---|---|---|---|---|
| G1 | **Sync des nouvelles connexions dans un CRM** | Connexion acceptée → fiche CRM + message de bienvenue auto | webhook `new_relation` | Classic | Composite | 📘 |
| G2 | **Enrichissement CRM automatique** | Profil + entreprise → fiche CRM (Attio/HubSpot/Sheet) | `GET /users/{id}`, `/linkedin/companies/{id}` | Classic | Composite | 🤝📘 |
| G3 | **Connecter tout le LinkedIn de l'équipe** | Opérer plusieurs comptes en leur nom (répartir charge + couverture) | `GET /accounts`, hosted auth | Classic | Composite | ✅🤝 |
| G4 | **Monitoring de la santé des comptes** | Alerte en cas de déconnexion / checkpoint d'un compte | webhook `account_status`, `POST /accounts/{id}/reconnect` | Classic | Atomique | 📘 |

## Socle technique (transverse, "Bien démarrer")

| # | Sujet | Contenu | Provenance |
|---|---|---|---|
| S1 | **Connecter un compte LinkedIn** | Hosted Auth Wizard ou cookie `li_at` ; gérer les checkpoints (2FA, captcha, validation app, OTP) | 📘 |
| S2 | **Respecter les limites LinkedIn (anti-ban)** | Caps quotidiens (≈25/jour/compte conseillé), fenêtre horaire locale [07:30-19:30], délais aléatoires, répartition multi-comptes | 🤝 |
| S3 | **Raw proxy Voyager (avancé)** | Accéder à des endpoints LinkedIn internes non standardisés par Unipile | ✅ |

---

## Total

**~38 cas d'usage** sur 7 familles + 3 socles. Couvre l'intégralité de la surface API LinkedIn d'Unipile (account, messaging, invitations, posts/engagement, profils, search Classic/Sales Nav/Recruiter, jobs, webhooks, raw proxy).

**Déjà prouvé en prod chez nous** (✅/🤝) : A4, A6, B1-B3, C3, D4, D5, E1, F2, G2, G3 + socle S2/S3.

## Classification : ressource & cadence

Le lead magnet livre **deux types de ressources** :

- 🟢 **Skill MCP** — à lancer **depuis Claude**, pilote le MCP Unipile (`https://developer.unipile.com/mcp`). Pour les usages **one-shot / ponctuels** (je le fais quand j'en ai besoin, interactif).
- 🔵 **Script workflow** — Python appelant l'API REST Unipile, **déployable sur Modal** (cron/webhook), à la `forward-graph`. Pour les usages **récurrents / planifiés** (ça tourne tout seul).
- 🟣 **Les deux** — capacité pertinente dans les deux modes ; livrée en skill ET en script.

**Axe de tri = cadence** : one-shot → skill MCP ; récurrent → script workflow.

| # | Cas d'usage | Cadence | Ressource | Note |
|---|---|---|---|---|
| A1 | Prospects via Sales Navigator | One-shot | 🟢 Skill MCP | Variante 🔵 si "leads frais" sur recherche sauvegardée planifiée |
| A2 | Prospects via recherche Classic | One-shot | 🟢 Skill MCP | |
| A3 | Liste d'entreprises cibles (ABM) | One-shot | 🟢 Skill MCP | |
| A4 | Profils qui engagent un post | Les deux | 🟣 | One-shot : analyser un post précis · Récurrent : tracker vos posts en continu ✅ |
| A5 | Social listening (posts par mot-clé) | Récurrent | 🔵 Script | Veille continue d'un sujet |
| A6 | Enrichir une liste de prospects | Les deux | 🟣 | One-shot : enrichir un CSV · Récurrent : enrichir les nouvelles entrées CRM |
| B1 | Invitation automatique de votre cible | Récurrent | 🔵 Script | Drip quotidien avec quota (anti-ban) |
| B2 | Séquence invitation → message | Récurrent | 🔵 Script | Multi-jours + webhook acceptation |
| B3 | Relance automatique des sans-réponse (J+3) | Récurrent | 🔵 Script | Cron ✅🤝 |
| B4 | InMail aux profils hors réseau | One-shot | 🟢 Skill MCP | Au sein d'une séquence = script |
| B5 | Nettoyer les invitations en attente (withdraw) | Récurrent | 🔵 Script | Nettoyage périodique du quota |
| B6 | Auto-accepter les invitations reçues + bienvenue | Récurrent | 🔵 Script | Continu (webhook) |
| C1 | Sourcer des candidats | One-shot | 🟢 Skill MCP | À l'ouverture d'un poste ; variante pipeline continu = script |
| C2 | Entreprises qui recrutent (signal) | Récurrent | 🔵 Script | Scan hebdo de signaux 🤝 |
| C3 | Approche candidats automatisée | Récurrent | 🔵 Script | Séquence d'outreach |
| C4 | Publier / gérer une offre d'emploi | One-shot | 🟢 Skill MCP | |
| C5 | Pipeline d'une offre (applicants + CV) | Récurrent | 🔵 Script | Poll des candidats tant que le poste est ouvert |
| D1 | Publier un post par API | Les deux | 🟣 | One-shot : publier maintenant · Récurrent : calendrier éditorial planifié |
| D2 | Commenter / répondre automatiquement | Les deux | 🟣 | One-shot : commenter · Récurrent : auto-répondre aux commentaires de vos posts |
| D3 | Liker / réagir à des posts ciblés | Récurrent | 🔵 Script | Nurturing quotidien d'une liste |
| D4 | Performance de vos posts | Récurrent | 🔵 Script | Snapshot quotidien ✅ ; variante rapport one-shot |
| D5 | Veille de contenu concurrent / influenceur | Récurrent | 🔵 Script | Digest périodique ✅ |
| D6 | Activité publique d'un prospect (accroche) | One-shot | 🟢 Skill MCP | Prépa RDV |
| E1 | Qui a visité mon profil | Récurrent | 🔵 Script | Quotidien ✅ ; variante pull one-shot |
| E2 | Exporter tout votre réseau | One-shot | 🟢 Skill MCP | |
| E3 | Auditer followers & following | One-shot | 🟢 Skill MCP | Variante tracking de croissance = script |
| E4 | Suivre / ne plus suivre / bloquer | One-shot | 🟢 Skill MCP | Action ad-hoc |
| E5 | Recommander des compétences (endorse) | Récurrent | 🔵 Script | Campagne de nurturing |
| E6 | "Warm touch" : visite de profil déclenchée | Récurrent | 🔵 Script | Drip sur une liste cible |
| F1 | Inbox LinkedIn unifiée multi-comptes | Les deux | 🟣 | One-shot : lire mes messages depuis Claude · Récurrent : sync continue |
| F2 | Réponse temps réel (webhook → notif/IA) | Récurrent | 🔵 Script | Service webhook always-on ✅🤝 |
| F3 | Envoyer des pièces jointes en DM | One-shot | 🟢 Skill MCP | |
| F4 | Agir sur les messages (réagir/éditer/transférer/supprimer) | One-shot | 🟢 Skill MCP | |
| F5 | Suivre le cycle de vie des messages | Récurrent | 🔵 Script | Webhooks lu/livré/réaction |
| G1 | Sync des nouvelles connexions dans un CRM | Récurrent | 🔵 Script | Webhook `new_relation` |
| G2 | Enrichissement CRM automatique | Récurrent | 🔵 Script | Sur nouvelles entrées 🤝 ; variante batch one-shot |
| G3 | Connecter tout le LinkedIn de l'équipe | One-shot | 🟢 Skill MCP | Setup |
| G4 | Monitoring de la santé des comptes | Récurrent | 🔵 Script | Webhook `account_status` |
| S1 | Connecter un compte LinkedIn | One-shot | 🟢 Skill MCP | Setup guidé (hosted auth + checkpoints) |
| S2 | Anti-ban (limites LinkedIn) | Transverse | — | Brique partagée (`lib`) + garde-fou des scripts, pas une ressource isolée |
| S3 | Raw proxy Voyager (avancé) | Les deux | 🟣 | Brique avancée utilisable en skill ou script |

**Répartition** : 🟢 13 skills MCP (one-shot) · 🔵 20 scripts workflow (récurrent) · 🟣 5 les deux. (S2 = transverse.)

## Structure repo proposée (`forward-unipile`)

```
forward-unipile/
  README.md                    # Bien démarrer (S1 connexion, S2 anti-ban), MCP setup, prérequis
  .claude/skills/              # 🟢 Skills MCP (one-shot, pilotent le MCP Unipile)
    unipile-prospects-salesnav/SKILL.md + config.example.yaml
    unipile-enrichir-liste/    ...
    ...
  scripts/                     # 🔵 Scripts workflow (récurrent, REST API, Modal-ready)
    invitation_drip/           run.py + config + README (cron)
    relance_j3/                ...
    webhook_reponses/          ...
    ...
  lib/unipile_helpers.py       # client REST partagé : headers X-API-KEY, account_id, pagination, anti-ban (S2)
  examples/                    # sorties réelles (CSV/MD) par ressource
```

- **Skills MCP** : `SKILL.md` qui décrit le cas + pilote les tools du MCP Unipile (config légère). Pas de `run.py` nécessaire.
- **Scripts workflow** : Python via REST (`lib/unipile_helpers.py`), déployables Modal (cron/webhook), avec garde-fous anti-ban intégrés (S2). Réutilise les patterns prouvés de `forward-graph`.

## Prochaine étape

`/dev-scope` pour produire la spec du repo : valider la capacité d'écriture du MCP (cf. hypothèse), figer le contrat des skills/scripts, lister les briques `lib`, et planifier l'implémentation incrémentale (commencer par les ressources déjà prouvées en prod).
