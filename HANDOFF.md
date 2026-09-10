# Handoff per Claude Code

Stato al 10 settembre 2026, sera. La lezione è il 15 settembre.

## Fatto in questa sessione

I sei punti dell'handoff precedente sono chiusi.

1. **QA visivo del deck**: tutte le slide convertite in PDF e riviste una per
   una. Correzioni nello script, non nel pptx: allineamento della riga con il
   nome sulla copertina, riquadri di codice che sfioravano il footer, un "2"
   isolato a capo, un accento e una elisione. `image_top_bullets` ora riduce da
   sola l'altezza della figura quando i bullet non ci starebbero.
2. **Dodici esempi reali importati**. L'importatore spezzava ogni paragrafo del
   docx: ne produceva 43 invece di 12. Ora separa sui paragrafi numerati e
   legge le tabelle nella posizione giusta. Canale e mittente controllati a
   mano. Le richieste sono in `data/richieste.jsonl` come `RE01`-`RE12`, con le
   etichette in `data/etichette_oro.jsonl`. Il docx e il jsonl grezzo restano
   in `data/reali/`, fuori dal repository.
3. **Pipeline eseguita con la chiave vera** (gpt-5-mini, 40 richieste).
   L'esecuzione è congelata in `demo/output_esempio/`, valutazione compresa.
4. **URL del repository**: segnaposto esplicito `<da completare>` sulla slide
   "Materiali e contatti", con nota del relatore.
5. **Normativa verificata** su fonti reali. Resta un solo `[VERIFICARE]`, sulla
   DPIA, che è una decisione organizzativa.
6. **Repository git ricostruito** (il `.git` era dentro lo zip, non nella
   cartella). Quattro commit nuovi. Il push non è stato fatto.

## Poi, su richiesta

Il deck è passato da 41 a 97 slide con 62 immagini: 18 diagrammi e 44
fotografie generate con gpt-image-1, dodici delle quali servono a far
sorridere. Contenuto aggiunto, non riempitivo: il glossario per leggere
un'offerta, i canali e gli stati, cosa hanno insegnato i dodici esempi reali,
il quadro normativo in quattro slide, i quattro passi del pilota uno per slide.

Il materiale non presuppone più un DPO, che la Fondazione non ha.

## Da fare

1. **Sostituire `<da completare>` con l'account GitHub** in
   `slides/tools/build_deck.py`, poi rigenerare il deck. È l'unico segnaposto
   rimasto nel deck.
2. **Push**. Il comando è in fondo a questo file.
3. **Riscrivere la tassonomia sui corsi veri della Fondazione.** Dieci delle
   dodici richieste reali hanno corso `nessuno`, e tre sono commerciali
   (preventivi, sconti, MEPA) senza una voce dedicata. È il lavoro che vale di
   più prima della lezione, e si fa guardando il catalogo.
4. **Provare i tempi.** 97 slide in due ore, di cui trenta minuti di
   esercitazione, fanno circa un minuto a slide. Molte sono immagini da dieci
   secondi, ma vale la pena cronometrare almeno i blocchi 2 e 3.
5. Facoltativo: un costo per mille richieste da citare in aula. Nella slide
   "Quanto costa davvero" c'è un `[NEEDS SOURCE]` nelle note.

## Numeri da citare, misurati e non stimati

Esecuzione del 10 settembre 2026, gpt-5-mini, 40 richieste, etichette scritte
a mano. Dettaglio in `demo/output_esempio/valutazione.json`.

| Campo | Accuratezza |
|---|---|
| corso | 100% |
| tipologia | 85% |
| operatore | 85% |
| urgenza | 72,5% |
| tutti e quattro insieme | 60% |

Il numero che conta è un altro: **nessuna richiesta è scesa sotto la soglia di
confidenza di 0,7**, quindi tutte e 40 sono state assegnate in automatico,
comprese le 16 che avevano almeno un campo sbagliato. Il backend `mock` a
parole chiave si ferma al 38,5%.

## Vincoli da rispettare

- Lezione in italiano; niente trattini lunghi nei testi.
- Max 3 bullet per slide; slide sdoppiate con "Titolo 1/n". Lo script lo impone
  con un assert: non rimuoverlo.
- Gli operatori nella tassonomia sono ruoli, non persone.
- Non inventare numeri, fonti o articoli di legge: segnaposto o `[NEEDS SOURCE]`.
- Il deck si rigenera con `python slides/tools/build_deck.py`, mai a mano.
- `data/reali/` resta fuori dal repository pubblico.
- Le fotografie sono sintetiche: la nota della prima slide dice di dirlo in aula.

## Comandi

Rigenerare tutto:

```bash
python slides/tools/figure.py      # diagrammi e grafici
python slides/tools/build_deck.py  # deck
python -m pytest -q
```

Le fotografie non si rigenerano a ogni build: sono versionate. Per rifarle
serve `OPENAI_API_KEY` e `python slides/tools/foto.py --tutte`.

Push, da eseguire dopo aver creato il repository su GitHub:

Il branch locale si chiama `master`. GitHub oggi usa `main` come predefinito,
quindi conviene rinominarlo prima del primo push.

```bash
git branch -m master main
git remote add origin git@github.com:<utente>/promopa-agenti-ai.git
git push -u origin main
```

Se preferite tenere `master`, saltate la prima riga e usate
`git push -u origin master`.
