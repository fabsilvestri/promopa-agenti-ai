# Quadro normativo per il blocco 4 (note del docente)

Non è un parere legale. Serve a dire in aula cosa vale e cosa va deciso
dalla Fondazione prima di partire con un pilota.
Aggiornato al 10 settembre 2026. I punti marcati [VERIFICARE] restano
decisioni organizzative, non domande sul testo delle norme.

La Fondazione oggi non ha un responsabile della protezione dei dati. Il primo
passo del pilota, quindi, è stabilire chi risponde di queste decisioni: se
serva nominarne uno, se basti un consulente esterno per il pilota, o se il
punto di riferimento sia il legale che segue la Fondazione. Finché la casella
è vuota, i punti qui sotto restano aperti e nessuno li chiude per inerzia.

## AI Act (Reg. UE 2024/1689), come modificato dall'AI Omnibus (Reg. UE 2026/1744)

Il regolamento omnibus è stato pubblicato in Gazzetta il 24 luglio 2026 ed è
in vigore dal 27 luglio 2026. È la prima modifica sostanziale all'AI Act.

- **Art. 4, alfabetizzazione**: l'obbligo si applica dal 2 febbraio 2025 e la
  data non è cambiata. L'omnibus ha però riscritto l'articolo: da obbligo di
  garantire un livello adeguato di competenza a obbligo di adottare misure
  che sostengano lo sviluppo dell'alfabetizzazione, proporzionate al rischio.
  In pratica è passato da obbligo di risultato a obbligo di mezzi, e il testo
  chiarisce che non si deve garantire un livello determinato per ogni persona.
  Le lezioni di giugno e di oggi sono una di quelle misure.
- **Art. 50, trasparenza**: applicabile dal 2 agosto 2026, non rinviato
  dall'omnibus. Unica finestra transitoria, fino al 2 dicembre 2026, per la
  marcatura leggibile dalla macchina dei contenuti dei sistemi generativi già
  sul mercato. Rilevante per l'helpdesk: se un sistema di AI interagisce
  direttamente con le persone, va detto. Nel nostro disegno la bozza la invia
  un operatore, quindi l'interazione resta umana; se in futuro si attivasse
  una risposta automatica, scatterebbe l'obbligo di informare.
- **Alto rischio (Allegato III)**: gli obblighi slittano dal 2 agosto 2026 al
  2 dicembre 2027. Per i sistemi integrati in prodotti già coperti dalla
  normativa di armonizzazione su salute e sicurezza si passa dal 2 agosto 2027
  al 2 agosto 2028.
- **Perché lo smistamento non è ad alto rischio**: il punto 3 dell'Allegato III
  (istruzione e formazione professionale) elenca quattro usi, tutti sulla
  persona che studia: decidere accesso o ammissione a un istituto, valutare i
  risultati dell'apprendimento, stabilire il livello di istruzione a cui una
  persona può accedere, sorvegliare comportamenti vietati durante gli esami.
  Smistare una richiesta amministrativa a un ufficio non è nessuno dei quattro.
  L'unica voce dell'Allegato III che assomiglia a una classificazione di
  richieste in arrivo è il punto 5, lettera d, ma riguarda le chiamate di
  emergenza e la priorità nell'invio dei soccorsi.

## Legge 23 settembre 2025, n. 132 (legge italiana sull'IA)

- **Art. 14, uso dell'intelligenza artificiale nella pubblica amministrazione**.
  I tre commi dicono, in sintesi: le PA usano l'IA per efficienza, tempi e
  qualità dei servizi, assicurando conoscibilità del funzionamento e
  tracciabilità dell'utilizzo; l'uso è strumentale e di supporto all'attività
  provvedimentale, e la persona resta l'unica responsabile dei provvedimenti e
  dei procedimenti in cui l'IA è stata usata; le amministrazioni adottano
  misure tecniche, organizzative e formative per un utilizzo responsabile.
- Per la Fondazione: documentare che l'assegnazione automatica è rivedibile
  e che l'invio è umano copre gran parte del principio. La formazione del
  personale è essa stessa una delle misure richieste dal comma 3.
- Promo PA Fondazione non è una pubblica amministrazione, quindi l'art. 14 non
  la vincola in proprio. Lo citiamo perché è il metro con cui gli enti clienti
  guarderanno un servizio che smista le loro richieste.

## Linee guida AgID per l'adozione dell'IA nella PA

- Titolo: "Linee guida per l'adozione di IA nella pubblica amministrazione",
  approvate in sede di Conferenza Unificata il 10 settembre 2025.
- Impostazione per passi: valutazione del livello di maturità, valutazione dei
  rischi e degli impatti, progettazione e governance, indicatori di prestazione
  e monitoraggio. Il "pilota in quattro passi" ricalca questa struttura di
  proposito.
- Insistono su dati, misurazione e revisione periodica. Da citare a supporto
  del blocco 5.

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
  [VERIFICARE, e prima ancora decidere chi la firma].
- Se serva o no nominare un responsabile della protezione dei dati non è una
  domanda a cui rispondo qui: dipende da attività principale e scala del
  trattamento. È la prima cosa da chiedere a un legale, prima del pilota
  e indipendentemente da questo progetto.

## Cosa dire in aula, in tre frasi

1. Alfabetizzazione e trasparenza sono già obbligatorie; alto rischio no, e
   questo caso non lo è.
2. Finché l'invio resta umano, siete nel perimetro più semplice.
3. Il registro dei trattamenti e il DPA con il fornitore sono i due documenti
   da sistemare prima del pilota, non dopo. E prima ancora serve una persona
   che se ne prenda la responsabilità: oggi in Fondazione non c'è.

## Fonti consultate il 10 settembre 2026

- Reg. (UE) 2024/1689 (AI Act), Allegato III, punti 3 e 5:
  https://artificialintelligenceact.eu/annex/3/
- Reg. (UE) 2026/1744 (AI Omnibus), date di applicazione e art. 4 e 50:
  https://www.advant-nctm.com/en/news/digital-omnibus-on-ai-il-consiglio-adotta-il-regolamento-di-semplificazione-dellai-act
  e https://www.federprivacy.org/informazione/primo-piano/ai-omnibus-in-vigore-dal-27-luglio-2026-cambiano-le-scadenze-dell-ai-act-ma-gli-obblighi-di-trasparenza-restano-confermati
- L. 132/2025, art. 14, testo dei commi:
  https://www.statocitta.it/home/approfondimenti/tematiche-di-interesse/l-intelligenza-artificiale-ia-nella-pa/la-normativa-italiana-la-legge-1322025/
  e https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2025-09-23;132
- Linee guida AgID, titolo e approvazione in Conferenza Unificata:
  https://www.statocitta.it/home/approfondimenti/tematiche-di-interesse/l-intelligenza-artificiale-ia-nella-pa/le-linee-guida-per-l-adozione-della-ia-nella-pa/

Il testo consolidato dell'AI Act dopo l'omnibus non è stato letto
direttamente: le date qui sopra vengono da due fonti secondarie concordi.
Prima della lezione vale la pena aprire una volta l'EUR-Lex.
