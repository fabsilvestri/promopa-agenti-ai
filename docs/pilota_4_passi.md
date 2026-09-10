# Dal caso d'uso al pilota in quattro passi

## 1. Audit del flusso attuale (1-2 settimane)
- Contare: richieste al mese per canale (oggi: circa 300 su 5 caselle, più
  moduli sito e Moodle; Zoom e questionari non contati perché persi).
- Cronometrare: tempo medio dalla ricezione alla prima risposta, per tipologia.
- Disegnare: la griglia di scomposizione compilata per l'helpdesk.

## 2. Tassonomia e dati etichettati (2 settimane)
- Scrivere `tassonomia.yaml` con chi risponde davvero alle richieste.
- Etichettare a mano 100-200 richieste storiche (due persone, poi confronto:
  dove le due persone non concordano, la tassonomia è ambigua).
- Questo dataset è il metro. Senza, "funziona bene" è un'opinione.

## 3. Prototipo a basso codice (2-4 settimane)
- Un contenitore unico: anche un foglio condiviso o un ticketing gratuito.
- Connettori: caselle e-mail e moduli sito verso il contenitore
  (Make, Zapier, n8n, o script). Nessuna AI in questo passo.
- Classificazione: GPT personalizzato o la pipeline di questo repository.
- Coda "da verificare" per confidenza sotto soglia. L'invio resta umano.

## 4. Misurare per un mese, poi decidere
- Accuratezza per campo sul set etichettato (obiettivo indicativo: > 90% su
  tipologia e operatore; sotto l'80% il sistema fa perdere tempo).
- Tempo alla prima risposta: prima e dopo.
- Ore di segreteria a settimana sullo smistamento: prima e dopo.
- Quota di richieste andate alla coda umana (se supera il 30%, la tassonomia
  va rivista, non il modello).

Le soglie sopra sono punti di partenza, non standard: vanno fissate dalla
Fondazione prima di partire, non dopo aver visto i risultati.
