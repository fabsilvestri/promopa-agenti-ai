# Demo dal vivo (blocco 3, 30 minuti)

Due strade, stessa logica:

1. **Senza codice** (10 min): GPT personalizzato in ChatGPT Business.
   Istruzioni in `gpt_personalizzato/istruzioni.md`.
2. **Con codice** (10 min): pipeline Python.

        cd src
        HELPDESK_BACKEND=mock python -m helpdesk_agent.pipeline     # senza chiave, regole grezze
        python -m helpdesk_agent.pipeline --bozze                    # con OPENAI_API_KEY

   Il mock arriva circa al 50% di richieste completamente corrette; il modello
   vero molto più in alto. Mostrare la differenza è il punto: si misura, non si stima.

3. **Discussione** (10 min): aprire `demo/output/coda_per_operatore.md` e
   ragionare su cosa vedrebbe ogni operatore la mattina.

Piano B senza rete: `output_esempio/`.
