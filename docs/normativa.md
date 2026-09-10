# Quadro normativo per il blocco 4 (note del docente)

Non è un parere legale. Serve a dire in aula cosa vale e cosa va verificato
con il DPO della Fondazione prima di partire con un pilota.
Aggiornato al 10 settembre 2026. I punti marcati [VERIFICARE] vanno
ricontrollati sul testo ufficiale prima della lezione.

## AI Act (Reg. UE 2024/1689), come modificato dall'AI Omnibus (Reg. UE 2026/1744)

- **Art. 4, alfabetizzazione**: dal 2 febbraio 2025 chi usa sistemi di AI deve
  assicurare un livello adeguato di competenza al personale. Le lezioni di
  giugno e di oggi sono, in pratica, parte dell'adempimento.
- **Art. 50, trasparenza**: applicabile dal 2 agosto 2026, non rinviato
  dall'Omnibus. Rilevante per l'helpdesk: se un sistema di AI interagisce
  direttamente con le persone, va detto. Nel nostro disegno la bozza la
  invia un operatore, quindi l'interazione resta umana; se in futuro si
  attivasse una risposta automatica, scatterebbe l'obbligo di informare.
- **Alto rischio (Allegato III)**: obblighi rinviati al 2 dicembre 2027
  dall'Omnibus in vigore dal 27 luglio 2026. Lo smistamento di richieste di
  un helpdesk formativo non rientra negli usi ad alto rischio elencati
  [VERIFICARE con il DPO: l'"istruzione e formazione professionale" è in
  Allegato III, ma per accesso e valutazione degli studenti, non per lo
  smistamento amministrativo].

## Legge 23 settembre 2025, n. 132 (legge italiana sull'IA)

- Principi generali: supervisione umana, tracciabilità, responsabilità
  che resta alla persona. Per la PA: l'AI supporta, la decisione resta al
  funzionario [VERIFICARE numero dell'articolo sulla PA nel testo vigente].
- Per la Fondazione: documentare che l'assegnazione automatica è rivedibile
  e che l'invio è umano copre gran parte del principio.

## Linee guida AgID per l'adozione dell'IA nella PA (2025)

- Approccio per fasi: analisi del contesto, valutazione dei rischi,
  progettazione, monitoraggio. Il "pilota in quattro passi" ricalca
  questa struttura di proposito.
- Insistono su dati, misurazione e revisione periodica. Da citare a
  supporto del blocco 5.

## GDPR

- Le richieste contengono dati personali di dipendenti pubblici (nome, ente,
  a volte situazioni personali: malattia, contenziosi).
- Base giuridica: esecuzione del contratto formativo / interesse legittimo
  per lo smistamento. Da verbalizzare nel registro dei trattamenti.
- Responsabile del trattamento: il fornitore del modello (OpenAI per ChatGPT
  Business e API). Verificare il DPA e la sede di trattamento dei dati.
- Minimizzazione: al modello serve il testo della richiesta, non lo storico
  del mittente. La pipeline in questo repository passa solo il testo.
- DPIA: probabilmente non obbligatoria per lo smistamento, ma consigliata se
  si aggiungono profilazione del mittente o risposte automatiche
  [VERIFICARE con il DPO].

## Cosa dire in aula, in tre frasi

1. Alfabetizzazione e trasparenza sono già obbligatorie; alto rischio no, e
   questo caso non lo è.
2. Finché l'invio resta umano, siete nel perimetro più semplice.
3. Il registro dei trattamenti e il DPA con il fornitore sono i due documenti
   da sistemare prima del pilota, non dopo.
