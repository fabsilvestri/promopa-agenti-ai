# Output di esempio

Esecuzione completa della pipeline con `gpt-5-mini` sulle 40 richieste del
repository, il 10 settembre 2026: 31 richieste strutturate (19 sintetiche e 12
reali della Fondazione) più 9 estratte da chat Zoom e questionari Moodle.

Serve per la demo se manca la rete, e i grafici del deck si rigenerano da qui
senza chiave API.

| File | Contenuto |
|---|---|
| `richieste_classificate.jsonl` | Una riga per richiesta, con classificazione e bozza |
| `richieste_classificate.csv` | Le stesse righe, per aprirle in un foglio |
| `coda_per_operatore.md` | Quello che ogni ruolo vedrebbe la mattina |
| `valutazione.json` | Accuratezza per campo, errori, confidenza per richiesta |

## Cosa dice la valutazione

| Campo | Accuratezza |
|---|---|
| corso | 100% |
| tipologia | 85% |
| operatore | 85% |
| urgenza | 72,5% |
| tutti e quattro insieme | 60% |

Il dato che conta di più non è l'accuratezza: è che **nessuna richiesta è
scesa sotto la soglia di confidenza di 0,7**. La confidenza minima dichiarata
è stata 0,75, quindi tutte e 40 sono state assegnate in automatico, comprese
le 16 che avevano almeno un campo sbagliato. Il punto di controllo automatico,
da solo, non ha fermato niente.

Note su alcune richieste:

- **RE01**: il partecipante ha finito il corso ma la piattaforma non gli fa
  scaricare l'attestato. Il modello dice `attestato`, l'etichetta di
  riferimento dice `accesso-piattaforma`. Non è ovvio chi abbia ragione: è il
  caso da portare a un umano.
- **RE12**: non è una richiesta, è l'avviso automatico di una casella
  dismessa. Il modello la classifica come `informazioni` e la manda alla
  segreteria.
- **Urgenza**: 11 errori su 40. È il campo dove anche due persone della
  segreteria non sarebbero d'accordo.

Per rigenerarlo con il tuo modello:

    export OPENAI_API_KEY=...
    cd src && python -m helpdesk_agent.pipeline --bozze --out ../demo/output
