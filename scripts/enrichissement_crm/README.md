# 🔵 enrichissement_crm (G2)

Enrichit une liste de profils (ex. nouvelles entrées CRM) : profil + entreprise → fiche
poussée dans le CRM. **CRM générique** : `to_crm()` est un stub à câbler. Lecture LinkedIn.

- **Cadence** : récurrent (cron, ou déclenché sur nouvelles entrées).
- **Endpoints** : `GET /users/{id}`, `GET /linkedin/companies/{id}`.

## Lancer

```bash
python scripts/enrichissement_crm/run.py --config scripts/enrichissement_crm/config.example.yaml
```

## Déployer (Modal, cron)

```python
@app.function(image=image, schedule=modal.Cron("0 7 * * *"), secrets=[modal.Secret.from_name("unipile")])
def daily():
    from run import run, u
    run(u.load_config("config.example.yaml"))
```

Câbler `to_crm()` à votre CRM (Attio, HubSpot, Google Sheet...).
