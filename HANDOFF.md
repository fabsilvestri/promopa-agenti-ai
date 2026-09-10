# Handoff per Claude Code

Stato all'11 settembre 2026. La lezione è il 15 settembre, **da remoto**.

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
5. **Blocco normativo riscritto per non esporre il docente.** Le conclusioni
   giuridiche sono state tolte tutte: il materiale non dice più se una norma si
   applica al caso della Fondazione, non cita articoli sulle slide e non
   prescrive adempimenti. Al loro posto ci sono una slide di premessa esplicita
   ("sono un informatico, non un avvocato") e sei domande da girare per iscritto
   a chi ha titolo per rispondere. `docs/normativa.md` è diventato
   `docs/domande_legali.md` e ha la stessa impostazione.
6. **Repository git ricostruito** (il `.git` era dentro lo zip, non nella
   cartella). Quattro commit nuovi. Il push non è stato fatto.

## Poi, su richiesta

Il deck è passato da 41 a 97 slide con 86 immagini: 78 fotografie generate con
gpt-image-1 e 8 fra tabelle e grafici fatti con matplotlib. Contenuto aggiunto,
non riempitivo: il glossario per leggere un'offerta, i canali e gli stati, cosa
hanno insegnato i dodici esempi reali, i quattro passi del pilota uno per slide.

Poi una seconda passata sullo stile:

- Titoli in blu notte invece del bordeaux del template. Il filetto del footer e
  il logo Sapienza restano bordeaux e fanno da accento.
- Corpo dei bullet più grande su tutti i layout.
- Nessuna slide è più di soli bullet: le ventiquattro che sembravano vuote
  hanno una fotografia scelta sul contenuto.
- I diagrammi a riquadri sono diventati fotografie con le etichette vere
  sopra. Il modello non sa scrivere testo leggibile, quindi la disposizione la
  dà la foto e le parole le mette PowerPoint. Le targhette dei passi con un
  modello dentro si accendono in blu pieno.
- Tabelle e grafici restano matplotlib, ristilizzati: intestazione blu piena,
  niente righe verticali, righe alternate.
- Dissolvenza fra le slide, più lenta sui cambi di blocco. Comparsa
  progressiva dei bullet su diciotto slide, quelle dove ogni riga è un passo.

## Il blocco 6 è stato rifatto per il remoto

Le stanze separate da remoto, con dipendenti pubblici spesso senza telecamera,
producono silenzio: nessuno si offre di scrivere e chi conduce non può girare
fra i tavoli. Il blocco ora è:

| Tempo | Cosa succede |
|---|---|
| 10 minuti | ognuno compila la griglia da solo, microfoni chiusi |
| 15 minuti | si scompone dal vivo un processo scelto fra i loro, riga per riga |
| 5 minuti | le tre domande finali, una riga a testa in chat |

Il punto che le stanze servivano a insegnare non si perde, anzi si vede meglio:
quando si arriva alla colonna Tipo si chiede alla chat "AI o umano?" e le
risposte divergenti dimostrano dal vivo che dove due persone non concordano il
problema è la tassonomia. È la stessa frase del blocco 4, sul loro processo.

A fine giornata la chat va salvata: è un elenco di processi candidati scritto
dal personale della Fondazione, e vale più delle slide.

Attesi meno di quindici collegati, quindi la chat si legge mentre si parla e si
possono chiamare le persone per nome. Sopra le cinquanta il blocco andrebbe
ripensato con sondaggi al posto del testo libero.

Il materiale non presuppone più un DPO, che la Fondazione non ha, e non lo
dichiara neppure come mancanza: la slide chiede chi risponde delle decisioni sui
dati, in forma condizionale.

## Da fare

1. **Decidere se il repository resta privato.** Oggi è privato, quindi il link
   sulla slide "Materiali e contatti" dà 404 a chi non è invitato. Prima della
   lezione: renderlo pubblico, invitare i partecipanti, o togliere la riga.
   Il comando è in fondo a questo file.
3. **Riscrivere la tassonomia sui corsi veri della Fondazione.** Dieci delle
   dodici richieste reali hanno corso `nessuno`, e tre sono commerciali
   (preventivi, sconti, MEPA) senza una voce dedicata. È il lavoro che vale di
   più prima della lezione, e si fa guardando il catalogo.
4. **Provare i tempi.** 97 slide in due ore, di cui trenta minuti di
   esercitazione, fanno circa un minuto a slide. Molte sono immagini da dieci
   secondi, ma vale la pena cronometrare almeno i blocchi 2 e 3.
5. **Far leggere il blocco 4 a un legale**, se ne avete uno a disposizione.
   Non per farlo correggere, ma per sapere se anche in forma di domanda c'è
   qualcosa che conviene togliere.
6. Facoltativo: un costo per mille richieste da citare in aula. Nella slide
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
- **Niente conclusioni giuridiche, mai.** Non scrivere su una slide se una norma
  si applica, se un obbligo scatta, se un adempimento è dovuto o se un caso
  rientra in una categoria. Il docente è un informatico e quelle frasi, dette in
  aula davanti a dipendenti pubblici, diventano sue. Le norme si nominano, le
  domande si formulano, le risposte le dà un giurista.
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

Le fotografie non si rigenerano a ogni build: sono versionate. Per rifarne una
serve `OPENAI_API_KEY` e `python slides/tools/foto.py --solo <nome>`; per
rifarle tutte, `--tutte`.

Se PowerPoint dovesse lamentarsi delle animazioni, in fondo a
`slides/tools/build_deck.py` si tolgono le due righe che chiamano
`_costruzione` e `_transizione`: il deck resta identico, senza effetti.

Le etichette sopra le fotografie degli schemi hanno coordinate da 0 a 1 dentro
il riquadro della foto. Se una foto viene rigenerata, gli oggetti si spostano e
le etichette vanno rimisurate: si rende il PDF, si ritaglia la fascia e ci si
mette sopra una griglia.

Push, da eseguire dopo aver creato il repository su GitHub:

Il repository è `github.com/fabsilvestri/promopa-agenti-ai`, privato, branch
`main`. Per renderlo pubblico prima della lezione:

```bash
gh repo edit fabsilvestri/promopa-agenti-ai --visibility public --accept-visibility-change-consequences
```

Attenzione a cosa diventa pubblico: le dodici richieste vere della Fondazione,
anche se anonimizzate, e le frasi sulla loro situazione interna. Il docx
originale resta comunque fuori, è in `.gitignore`.
