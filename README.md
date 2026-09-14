# Agenti AI per i processi interni

Materiale della lezione per Promo PA Fondazione, 15 settembre 2026, da remoto.
Docente: Fabrizio Silvestri (Sapienza, DIAG). Caso di studio: helpdesk formazione.

## Struttura

| Cartella | Contenuto |
|---|---|
| `slides/` | Il deck (`Lezione_15_settembre_Agenti_AI_PromoPA.pptx`, 100 slide) e gli script che lo generano (`tools/`) |
| `data/` | Tassonomia, richieste sintetiche, grezzi Zoom/Moodle, etichette di riferimento |
| `src/helpdesk_agent/` | Pipeline: estrazione, classificazione con output strutturato, bozze, valutazione |
| `demo/` | Istruzioni per il GPT personalizzato, sequenza della demo, output di esempio |
| `esercitazione/` | Griglia di scomposizione e processi candidati |
| `docs/` | Pilota in quattro passi, domande da girare a un legale |
| `SCRIPT.md` | Lo svolgimento della lezione, slide per slide, con la demo alla lettera |
| `SCRIPT.docx` | Lo stesso, impaginato per essere letto o stampato. Si rigenera, non si modifica |
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

Per la demo dal vivo, tre comandi che stanno nei tempi di un'aula:

```bash
cd src
HELPDESK_BACKEND=mock python -m helpdesk_agent.pipeline     # istantaneo
python -m helpdesk_agent.pipeline --solo-grezzi             # ~60 s, Zoom e Moodle
python -m helpdesk_agent.una --bozza "il testo di una richiesta"   # ~14 s
```

`--limite N` ferma la pipeline dopo N richieste, `--paralleli N` decide quante
ne lavora insieme. Tutto lo svolgimento della lezione, parola per parola, è in
[SCRIPT.md](SCRIPT.md).

Output in `demo/output/`: CSV, JSONL e `coda_per_operatore.md`.

## Rigenerare le slide

```bash
pip install python-pptx matplotlib pillow
python slides/tools/figure.py      # 18 fra diagrammi, tabelle e grafici
python slides/tools/build_deck.py  # deck da Template_RSTLess.pptx
python slides/tools/script_docx.py # SCRIPT.docx da SCRIPT.md
```

Le 79 fotografie in `slides/tools/fig/foto/` sono generate una volta sola con
`slides/tools/foto.py` (gpt-image-1, serve `OPENAI_API_KEY`) e poi versionate:
il deck si ricostruisce senza rigenerarle. Sono immagini sintetiche e la nota
del relatore della prima slide dice di dirlo in aula.

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
6. Esercitazione individuale, scomposizione dal vivo, restituzione in chat (30')
