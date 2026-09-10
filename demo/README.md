# Demo dal vivo (blocco 3, 30 minuti)

Due strade, stessa logica:

1. **Senza codice** (10 min): GPT personalizzato in ChatGPT Business.
   Istruzioni in `gpt_personalizzato/istruzioni.md`.
2. **Con codice** (10 min): pipeline Python.

        cd src
        HELPDESK_BACKEND=mock python -m helpdesk_agent.pipeline     # senza chiave, regole grezze
        python -m helpdesk_agent.pipeline --bozze                    # con OPENAI_API_KEY

   Sulle richieste del repository il mock (regole a parole chiave) arriva al
   38,5% di richieste completamente corrette, il modello al 60%. Mostrare la
   differenza è il punto: si misura, non si stima. I numeri completi
   dell'esecuzione del 10 settembre 2026 sono in `output_esempio/valutazione.json`.

   Attenzione al numero che conta di più: con il modello nessuna richiesta è
   scesa sotto la soglia di confidenza, quindi la coda umana non si è mai
   riempita, e 16 richieste sbagliate su 40 sono passate in automatico.

3. **Discussione** (10 min): aprire `demo/output/coda_per_operatore.md` e
   ragionare su cosa vedrebbe ogni operatore la mattina.

Piano B senza rete: `output_esempio/`.
