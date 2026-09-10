# Agenti AI per i processi interni

Materiale della lezione per Promo PA Fondazione, 15 settembre 2026.
Docente: Fabrizio Silvestri (Sapienza, DIAG). Caso di studio: helpdesk formazione.

## Struttura

| Cartella | Contenuto |
|---|---|
| `slides/` | Il deck (`Lezione_15_settembre_Agenti_AI_PromoPA.pptx`) e gli script che lo generano (`tools/`) |
| `data/` | Tassonomia, richieste sintetiche, grezzi Zoom/Moodle, etichette di riferimento |
| `src/helpdesk_agent/` | Pipeline: estrazione, classificazione con output strutturato, bozze, valutazione |
| `demo/` | Istruzioni per il GPT personalizzato, sequenza della demo, output di esempio |
| `esercitazione/` | Griglia di scomposizione e processi candidati |
| `docs/` | Pilota in quattro passi, note normative |
| `tests/` | Test sul backend mock (nessuna chiamata di rete) |

## Avvio rapido

```bash
pip install -r requirements.txt
python data/genera_dataset.py               # rigenera dati e grezzi
cd src
HELPDESK_BACKEND=mock python -m helpdesk_agent.pipeline          # senza chiave API
OPENAI_API_KEY=sk-... python -m helpdesk_agent.pipeline --bozze  # con modello
cd .. && python -m pytest -q
```

Output in `demo/output/`: CSV, JSONL e `coda_per_operatore.md`.

## Rigenerare le slide

```bash
pip install python-pptx matplotlib
python slides/tools/figure.py      # diagrammi in slides/tools/fig/
python slides/tools/build_deck.py  # deck da Template_RSTLess.pptx
```

Regola del deck: massimo tre bullet per slide; se servono di più, la slide
si sdoppia con titolo "Titolo 1/n". Lo script lo impone.

## Importare gli esempi reali

```bash
cp "Richieste a Promo PA Fondazione.docx" data/reali/
cd src && python -m helpdesk_agent.importa_docx "../data/reali/Richieste a Promo PA Fondazione.docx"
```

Lo script separa le richieste sui paragrafi numerati del documento e scrive
`data/reali/richieste_reali.jsonl` (ignorato da git, come il docx). Il canale
è una prima ipotesi da parole chiave e il mittente non c'è: vanno controllati
a mano prima di unire le richieste a `data/richieste.jsonl` e le etichette a
`data/etichette_oro.jsonl`.

I 12 esempi della Fondazione (id da `RE01` a `RE12`) sono già stati importati,
controllati e uniti. Il docx resta fuori dal repository.

## Scaletta (2 ore)

1. Riaggancio e tesi (10')
2. Anatomia di un sistema agentico (20')
3. Il caso helpdesk, scomposto, con demo (30')
4. Limiti e rischi (15')
5. Dal caso d'uso al pilota (15')
6. Esercitazione in gruppi e restituzione (30')
