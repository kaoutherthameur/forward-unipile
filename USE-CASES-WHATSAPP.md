# Forward Unipile x WhatsApp — Catalogue de cas d'usage

> Cadrage (2026-07-15). Cas d'usage permis par l'API **WhatsApp** d'Unipile, pour le kit `forward-unipile`, sur le même modèle que la partie LinkedIn (`USE-CASES.md`) : 1 ressource = 🟢 skill MCP one-shot ou 🔵 script workflow (cron/webhook).
> Angle : **ce que WhatsApp permet quand on le branche à une IA**. Complément WhatsApp de l'instance 2 du Kit Outils (la partie LinkedIn étant déjà couverte).

## LinkedIn vs WhatsApp : deux surfaces d'API différentes

Le repo couvre **un seul provider (Unipile), deux canaux**. Ils n'ont pas la même nature :

| | **LinkedIn** (`USE-CASES.md`) | **WhatsApp** (ce fichier) |
|---|---|---|
| Nature de l'API | Recherche + actions sociales (rechercher des profils, inviter, poster, liker, sourcer) | **Messagerie pure** (lire, envoyer, réagir, transférer) |
| Question type | "Trouve-moi / touche des gens que je ne connais pas encore" | "Gère les conversations avec des gens qui m'écrivent déjà" |
| Compte connecté | Compte LinkedIn réel (Classic / Sales Nav / Recruiter) | Compte **WhatsApp perso** connecté en QR (pas l'API Business officielle) |
| Cold outreach | Possible avec garde-fous (invitations, InMail) | **À éviter** : WhatsApp bannit vite le cold/volume. Rester conversationnel / opt-in / déclenché par événement |
| Cas d'usage phares | Prospection, outreach, recrutement, contenu, réseau | Service client, relance & suivi, coaching, productivité inbox |

**Conséquence de design** : les cas WhatsApp de ce kit sont tous **conversationnels ou opt-in** (quelqu'un t'écrit, un client existant, un coaché qui a accepté). On ne fait pas de prospection à froid en masse sur WhatsApp - c'est le meilleur moyen de faire bannir le compte.

## Sources

- **Doc officielle Unipile** : developer.unipile.com (endpoints messagerie unifiés, provider WhatsApp)
- **Partie LinkedIn du repo** : `lib/unipile_helpers.py` (client REST + garde-fous anti-ban), moules `docs/skill-template.md` et `docs/script-template.md`

## Légende

**Type** : 🟢 Skill MCP one-shot (`.claude/skills/whatsapp-{cas}/`) · 🔵 Script workflow (`scripts/whatsapp/{cas}/`, cron ou webhook)
**Endpoints WhatsApp** (via Unipile) : `GET /chats`, `GET /chats/{id}/messages`, `POST /chats/{id}/messages` (envoi), `POST /chats` (nouveau fil), webhook `message_received`, pièces jointes (image / doc / audio / note vocale).

---

## Famille A — Service client & support

| # | Cas d'usage | Bénéfice | Forme | Mécanisme |
|---|---|---|---|---|
| A1 | **Inbox WhatsApp → Slack/CRM en temps réel** | Chaque message entrant part en notif Slack + log CRM. Plus de message oublié. | 🔵 webhook | `message_received` → notif |
| A2 | **Réponse IA de premier niveau** | L'IA répond aux questions fréquentes (horaires, prix, dispo), escalade à un humain sinon. | 🔵 webhook | `message_received` → IA → `POST /chats/{id}/messages` |
| A3 | **Tri + étiquetage automatique des demandes** | Classer chaque conversation (SAV / commande / réservation / spam) et router. | 🔵 webhook | `message_received` → classif → routage |
| A4 | **Accusé de réception hors horaires** | "Bien reçu, on revient sous 2h" envoyé automatiquement en dehors des heures d'ouverture. | 🔵 webhook | fenêtre horaire → envoi auto |
| A5 | **Résumé d'une conversation client** | Reprendre un fil long → récap + prochaine action. | 🟢 skill | `GET /chats/{id}/messages` |
| A6 | **Détection de client mécontent / urgence** | Repérer les mots de churn ("annuler", "remboursement", "déçu") → alerte prioritaire. | 🔵 webhook | `message_received` → mots-clés → alerte |

## Famille C — Relance & suivi commercial

| # | Cas d'usage | Bénéfice | Forme | Mécanisme |
|---|---|---|---|---|
| C1 | **Rappel de RDV automatique** | J-1 et H-2 avant un rendez-vous → message de rappel (réduit le no-show). | 🔵 cron | fenêtres J-1/H-2 → envoi |
| C2 | **Relance devis / facture** | Devis sans réponse à J+N → relance douce. Facture impayée → rappel. | 🔵 cron | éligibilité J+N → envoi |
| C3 | **Suivi post-achat / onboarding** | Séquence bienvenue J0 → conseil J+2 → check J+7 pour un nouveau client. | 🔵 cron | étape due par jour → envoi |
| C4 | **Demande d'avis / NPS** | X jours après une prestation → demander une note + un avis Google. | 🔵 cron | délai → envoi |
| C5 | **Relance panier / réservation abandonnée** | Réservation ou panier non finalisé → un rappel unique. | 🔵 cron | événement + délai → envoi |

## Famille E — Coaching & accompagnement

| # | Cas d'usage | Bénéfice | Forme | Mécanisme |
|---|---|---|---|---|
| E1 | **Check-in quotidien / rituel** | "C'est fait, ton action du jour ?" chaque matin à un coaché. | 🔵 cron | matin → envoi |
| E2 | **Accountability bidirectionnel** | Le coaché répond son avancement → l'IA relance, encourage, log la progression. | 🔵 webhook | `message_received` → réponse + log |
| E3 | **Délivrance de programme en drip** | Un module / exercice par jour sur N semaines (pièce jointe possible). | 🔵 cron | module du jour → envoi |
| E4 | **Journal de bord du coaché** | Compiler les réponses de la semaine en un point de progression pour la séance. | 🟢 skill | `GET /chats/{id}/messages` |
| E5 | **Rappel d'exercice + collecte de preuve** | Demander une photo / audio de l'exercice fait (WhatsApp gère bien le média). | 🔵 cron | rappel → réception PJ (webhook) |
| E6 | **Transcription des notes vocales** | Le coaché envoie un vocal → transcription auto + résumé pour le coach. | 🔵 webhook | audio reçu → transcription + résumé |

## Famille G — Inbox & productivité interne

| # | Cas d'usage | Bénéfice | Forme | Mécanisme |
|---|---|---|---|---|
| G1 | **Recherche dans tout l'historique WhatsApp** | "Retrouve-moi ce que X m'a dit sur le budget." | 🟢 skill | `GET /chats`, `/chats/{id}/messages` |
| G2 | **Extraction d'infos structurées** | Parser les conversations → adresses, montants, RDV → CSV pour tableur/CRM. | 🟢 skill | `GET messages` → parsing |
| G3 | **To-do depuis WhatsApp** | Détecter les messages qui appellent une action → créer une tâche. | 🔵 webhook | `message_received` → tâche |
| G4 | **Inbox unifiée multi-canal** | WhatsApp + LinkedIn + Instagram + email dans une seule vue. | 🟢 skill | `GET /chats` (tous providers) |

---

## Hors scope (volontairement)

- **Prospection à froid en masse** sur WhatsApp (risque de ban du compte perso). Pour du cold, passer par LinkedIn (`USE-CASES.md`) ou l'API WhatsApp Business officielle (hors périmètre de ce kit).
- **Familles écartées au cadrage** (2026-07-15) : prospection WhatsApp (B), animation de communauté / groupes (D), notifications transactionnelles pures (F). Réintégrables plus tard si besoin.

## Sécurité & anti-ban (WhatsApp)

- Compte WhatsApp **perso** : respecter un rythme humain. Tout envoi en volume passe par les garde-fous de `lib/unipile_helpers.py` (plafond quotidien, fenêtre horaire locale, espacement aléatoire).
- Les écritures (envois) tournent en **`DRY_RUN` par défaut** (`UNIPILE_DRY_RUN=1`) : rien n'est envoyé tant que tu ne passes pas `UNIPILE_DRY_RUN=0`.
- Rester **opt-in** : n'écrire qu'à des gens qui t'ont écrit ou ont consenti (clients, coachés, leads entrants).
