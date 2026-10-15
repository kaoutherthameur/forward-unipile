# Transcription de note vocale WhatsApp - vocal -> résumé (exemple fictif)

_Illustratif. `transcribe()` et `summarize()` sont des stubs déterministes ; en prod_
_ils appellent un STT (Whisper) et un LLM._

## Payload webhook reçu (note vocale de Camille)

```json
{
  "event": "message_received",
  "chat_id": "c-3001",
  "sender": {"attendee_provider_id": "3361234...", "attendee_name": "Camille"},
  "attachment": {"type": "audio", "url": "https://exemple.test/vocal-camille.ogg"}
}
```

## Transcription (stub, illustratif)

> Coucou, alors aujourd'hui j'ai réussi à faire mes 30 minutes de rédaction sur mon
> offre, par contre je bloque encore sur le titre, j'ai testé trois versions mais
> aucune ne me satisfait, on pourra en parler à la séance ?

## Résumé pour le coach (stub, illustratif)

> Camille a fait ses 30 min de rédaction. Bloque sur le titre de l'offre (3 versions
> testées). Point à aborder en séance.

```
VOCAL RESUME: {"chat_id": "c-3001", "sender_name": "Camille", "summary": "Camille a fait ses 30 min de rédaction. Bloque sur le titre de l'offre (3 versions testées). Point à aborder en séance.", "transcript": "[transcription simulée de https://exemple.test/vocal-camille.ogg]"}
```
