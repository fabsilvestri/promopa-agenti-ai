# Handoff per Claude Code

Stato al 10 settembre 2026. Tutto ciò che è qui è stato costruito in una
sessione claude.ai; si continua da qui.

## Fatto
- Repo completo: dati, pipeline, test (4/4 verdi con backend mock), demo,
  esercitazione, docs, deck 41 slide dal template RSTLess (validato).
- Deck: fix applicati a footer, bullet nei titoli di sezione, ancoraggio
  del testo in alto; figure larghe messe sopra i bullet.

## Da fare
1. QA visivo finale del deck: convertire in PDF (`soffice --headless
   --convert-to pdf`) e guardare ogni slide; cercare overflow e sovrapposizioni.
   In particolare: slide titolo (riga con il nome sotto il riquadro azzurro),
   slide "L'architettura" e "Demo: il risultato" (didascalia vs footer).
2. Importare i 12 esempi reali di Matteo Baesso dal docx (vedi README),
   controllare le etichette, unirli a `data/richieste.jsonl` e alle
   `etichette_oro.jsonl`, rigenerare `demo/output_esempio` e la figura
   `tabella_demo.png`.
3. Eseguire la pipeline con OPENAI_API_KEY vera e aggiornare la slide
   "L'accuratezza si misura" con i numeri reali (oggi cita solo il mock al 50%).
4. Sostituire in "Materiali e contatti" la riga sul repository con l'URL GitHub.
5. Verificare i punti `[VERIFICARE]` in `docs/normativa.md` con il testo
   della L. 132/2025 e delle linee guida AgID.
6. `git remote add origin ...` e push.

## Vincoli da rispettare
- Lezione in italiano; niente trattini lunghi nei testi.
- Max 3 bullet per slide; slide sdoppiate con "Titolo 1/n".
- Gli operatori nella tassonomia sono ruoli, non persone.
- Non inventare numeri: dove mancano, segnaposto o "[NEEDS SOURCE]".
