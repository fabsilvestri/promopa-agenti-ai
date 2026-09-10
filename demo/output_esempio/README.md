# Output di esempio

Estratto di un'esecuzione della pipeline con modello OpenAI su 9 richieste
rappresentative (e-mail, modulo sito, chat Zoom, questionario Moodle).
Serve per la demo se manca la rete e per le slide.

Nota su Q06: confidenza 0,66, sotto la soglia di 0,7. Il sistema non assegna
e la richiesta resta in coda "da verificare": è un reclamo o un feedback?
Decide un umano. Questo è il comportamento voluto.

Per rigenerarlo con il tuo modello:

    export OPENAI_API_KEY=...
    cd src && python -m helpdesk_agent.pipeline --bozze --out ../demo/output
