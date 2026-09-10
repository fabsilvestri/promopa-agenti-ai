# Domande da girare a chi ha titolo per rispondere

## Premessa, da leggere prima di tutto il resto

Questo documento non è un parere legale e non vuole assomigliarci. Chi lo ha
scritto è un informatico. Non contiene, di proposito, nessuna affermazione su
quali norme si applichino al caso della Fondazione, su quali obblighi ne
discendano e su quali adempimenti siano o non siano dovuti.

Quelle sono qualificazioni giuridiche. Le fa un giurista, per iscritto, dopo
aver visto il progetto vero.

Quello che c'è qui dentro è due cose:

1. le domande che vale la pena mettere per iscritto prima di partire;
2. i riferimenti da cui partire per cercare, con la data in cui sono stati
   consultati e l'avvertenza che vanno riverificati sul testo ufficiale.

Se in aula arriva la domanda "quindi possiamo farlo?", la risposta non sta in
questo file. Sta nella risposta scritta di chi segue la Fondazione sul legale.

## Le sei domande

Sono formulate così perché una domanda scritta produce una risposta scritta, e
una risposta scritta protegge chi la riceve.

1. **Perimetro.** Il sistema che vogliamo costruire, cioè un classificatore che
   smista richieste in arrivo verso ruoli interni con un umano che rivede e
   invia, rientra fra quelli soggetti a obblighi rafforzati? Su quale base?
2. **Trasparenza verso chi scrive.** Dobbiamo informare chi ci manda una
   richiesta che una parte del processo usa AI? In quale momento, con quali
   parole, e cosa cambia se la revisione umana resta sempre presente?
3. **Base del trattamento.** Con quale base giuridica trattiamo il testo delle
   richieste per questa finalità, e dove va documentata?
4. **Fornitore.** Il fornitore del modello che ruolo assume rispetto ai nostri
   dati, quale contratto va firmato con lui, e dove vengono trattati i dati?
5. **Valutazione d'impatto.** Serve prima di partire? Se sì, chi la redige, chi
   la firma, e quando va rifatta?
6. **Automazione.** Cosa cambierebbe, in tutte le risposte precedenti, se un
   giorno la risposta partisse senza revisione umana?

## Chi risponde

Oggi in Fondazione non c'è una persona con questo ruolo assegnato. Prima della
tecnologia serve un nome accanto a queste decisioni. Se quel nome debba avere
un titolo formale, e quale, è la prima domanda da fare a un legale, ed è
indipendente da questo progetto.

## Riferimenti da cui partire

Consultati il 10 settembre 2026. Sono punti di partenza per una ricerca, non
una ricostruzione del quadro applicabile. Il testo consolidato su EUR-Lex non è
stato letto direttamente: le date qui sotto vengono da fonti secondarie
concordi fra loro, e vanno riverificate prima di citarle.

| Testo | Dove guardare |
|---|---|
| Regolamento (UE) 2024/1689, il cosiddetto AI Act | EUR-Lex, testo consolidato |
| Regolamento (UE) 2026/1744, che lo modifica | EUR-Lex; nel 2026 ha spostato più di una scadenza |
| Legge 23 settembre 2025, n. 132 | Normattiva, `urn:nir:stato:legge:2025-09-23;132` |
| Linee guida AgID per l'adozione di IA nella PA | agid.gov.it, approvate in Conferenza Unificata il 10 settembre 2025 |
| Allegato III dell'AI Act | artificialintelligenceact.eu/annex/3/ per una lettura rapida, poi EUR-Lex |

Note di lettura, senza conclusioni:

- L'AI Act è stato modificato nel 2026 e alcune date di applicazione si sono
  spostate. Qualsiasi scadenza letta in un articolo di giornale del 2025 va
  ricontrollata.
- L'Allegato III elenca casi d'uso. Leggerlo per capire di cosa parla è utile;
  decidere se un sistema ci rientra non è un esercizio di lettura.
- La legge 132/2025 contiene un articolo dedicato all'uso dell'IA nella
  pubblica amministrazione. Se la Fondazione ne sia destinataria diretta è una
  domanda da girare al legale, e comunque è il metro con cui gli enti clienti
  guarderanno un servizio che smista le loro richieste.

## Cosa il progetto fa, sul piano tecnico

Questi sono fatti sul codice, non affermazioni sulla conformità. Servono a chi
risponderà alle sei domande per sapere di cosa stiamo parlando.

- Al modello viene passato il testo della singola richiesta e la tassonomia.
  Non lo storico del mittente, non altre richieste, non archivi.
- La tassonomia contiene ruoli, non nomi di persone.
- Il modello produce campi strutturati e una bozza di risposta. Non invia
  niente e non ha accesso in scrittura a nessun sistema.
- La bozza contiene segnaposto espliciti dove il sistema non conosce un dato,
  invece di riempirli con un valore plausibile.
- Il documento dei dodici esempi reali era già anonimizzato all'origine: nomi e
  codici sostituiti da X.
