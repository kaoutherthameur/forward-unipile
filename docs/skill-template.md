# Moule : skill MCP 🟢 (one-shot)

Une skill = un dossier `.claude/skills/unipile-{cas}/` avec :

```
unipile-{cas}/
  SKILL.md             # frontmatter + sections imposées (ci-dessous)
  config.example.yaml  # config pré-remplie, sujet public/fictif
  (input.example.csv)  # si la skill prend une liste en entrée
```

La skill est lancée **depuis Claude** avec le **MCP Unipile** connecté (voir `CONNECTING-MCP.md`).
Elle pilote le MCP par intention ; si une action n'est pas exposée, fallback REST via `lib/unipile_helpers.py`.

## Structure imposée du `SKILL.md`

```markdown
---
name: unipile-{cas}
description: Use when [condition]. [entrée -> sortie].
---
# Titre

## Objectif & quand
Une phrase : pour qui, quel résultat, dans quel contexte one-shot.

## Prérequis
- Compte LinkedIn connecté à Unipile (+ abonnement requis : Classic / Sales Nav / Recruiter)
- MCP Unipile configuré (`CONNECTING-MCP.md`)

## Config
Champs de `config.example.yaml` (tableau champ -> rôle).

## Procédure (via MCP)
Étapes que Claude exécute en pilotant le MCP Unipile. Référencer l'endpoint
sous-jacent pour chaque étape (ex : `POST /linkedin/search`).

## Si le MCP ne fait pas l'action
Fallback REST : endpoint(s) exact(s) + `lib/unipile_helpers.py` à utiliser.

## Livrable
Format de sortie (CSV / markdown) + colonnes/sections.

## Limites & anti-ban
Quotas LinkedIn pertinents (lecture/écriture), précautions.

## Exemple
Pointeur vers `examples/{cas}.*`.
```
