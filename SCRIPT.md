# Script della lezione

Promo PA Fondazione, 15 settembre 2026, da remoto, due ore.
Cento slide. Docente: Fabrizio Silvestri.

## Come si legge questo documento

Per ogni slide ci sono tre cose.

- **Dire.** Il parlato. Dove è fra virgolette è pensato per essere detto così,
  non perché non si possa cambiare, ma perché quella formulazione è già stata
  pesata. Il resto è traccia.
- **Fare.** Le azioni: avanzare, condividere lo schermo, guardare la chat.
  Quando c'è scritto **[clic]** vuol dire che la slide ha un'animazione e il
  bullet successivo compare solo dopo un clic.
- **Note.** Quello che c'è nelle note del relatore dentro il pptx, in punti.

I tempi in testa a ogni blocco sono cumulativi dall'inizio.

Regola generale sul ritmo: le slide che sono solo una fotografia con una
didascalia durano dieci secondi. Non spiegarle. Servono a far respirare e a
cambiare argomento.

---

# Prima di cominciare

## Venti minuti prima

Una checklist, in quest'ordine.

1. **Aprire tre finestre e tenerle pronte**, in questo ordine da sinistra a
   destra sulla barra delle applicazioni:
   - PowerPoint con `slides/Lezione_15_settembre_Agenti_AI_PromoPA.pptx`,
     già in modalità presentatore
   - il browser con ChatGPT Business, GPT personalizzato già creato e aperto
     su una conversazione vuota
   - un terminale, già dentro la cartella giusta e già scaldato

2. **Scaldare il terminale.** Aprire il terminale e incollare esattamente
   questo, riga per riga:

   ```bash
   cd /Users/fabriziosilvestri/Documents/Codice/PromoPA-Lezione/src
   python -m helpdesk_agent.una "prova"
   ```

   Deve rispondere in una decina di secondi con una tabellina. Serve a due
   cose: verificare che la chiave API funzioni, e pagare adesso il costo del
   primo avvio di Python, che altrimenti si paga in aula.

   Se risponde `Backend: mock` invece di `Backend: openai`, la chiave non c'è.
   Controllare con `echo $OPENAI_API_KEY`. Se è vuota, aprire un terminale
   nuovo: la chiave sta in `~/.zshenv` e la leggono solo le shell nuove.

3. **Ingrandire il carattere del terminale.** Da remoto, su uno schermo
   condiviso, il corpo di default è illeggibile. Su macOS: Terminale, menu
   Vista, oppure `Cmd +` cinque o sei volte. Deve entrare comunque una riga da
   ottanta caratteri senza andare a capo.

4. **Preparare la chat.** Tenere pronti da incollare, in un file di testo a
   parte, questi tre messaggi:
   - il link alla griglia: `esercitazione/griglia_scomposizione.md`
   - le tre domande del blocco 6
   - le tre domande da fare a un fornitore (slide 24)

5. **Piano B.** Aprire in una scheda del browser
   `demo/output_esempio/coda_per_operatore.md` e
   `demo/output_esempio/valutazione.json`. Se la rete cade durante la demo si
   passa a quelli senza dire niente.

## I comandi della demo, in ordine

Sono tre. Sono già stati cronometrati. Vanno lanciati da
`/Users/fabriziosilvestri/Documents/Codice/PromoPA-Lezione/src`.

| # | Comando | Durata | Serve a |
|---|---|---|---|
| 1 | `HELPDESK_BACKEND=mock python -m helpdesk_agent.pipeline` | istantaneo | mostrare la forma dell'uscita e il 38,5% delle regole a parole chiave |
| 2 | `python -m helpdesk_agent.pipeline --solo-grezzi` | ~60 secondi | far vedere la chat Zoom che diventa righe di tabella |
| 3 | `python -m helpdesk_agent.una --bozza "<testo dettato in aula>"` | ~14 secondi | classificare dal vivo una richiesta scelta da loro |

Il terzo è il momento migliore della demo. Non saltarlo per fare in tempo:
semmai saltare il secondo.

Se serve tenere tutto sotto il minuto, il comando 2 diventa:

```bash
python -m helpdesk_agent.pipeline --solo-grezzi --limite 4
```

---

# La demo, parola per parola

Questa sezione è scritta per essere seguita alla lettera. Blocco 3,
slide 46-51, circa dodici minuti.

## Parte A. Senza codice, in ChatGPT (5 minuti)

### A.0 Prima della lezione: creare il GPT

Da fare una volta sola, non in aula.

1. ChatGPT Business, menu a sinistra, **Esplora GPT**, poi **Crea**.
2. Scheda **Configura**.
3. Nome: `Smistamento helpdesk formazione`.
4. Nel campo **Istruzioni** incollare il testo che sta in
   `demo/gpt_personalizzato/istruzioni.md`, dalla riga che comincia con
   "Sei il sistema di smistamento" fino a "non l'helpdesk." compreso.
   Non incollare i titoli in markdown né la parte "Sequenza consigliata".
5. In **Conoscenza**, caricare il file `data/tassonomia.yaml`.
6. In **Funzionalità**, lasciare acceso solo l'interprete di codice se c'è,
   spegnere navigazione e generazione immagini: non servono e rallentano.
7. Salvare come **Solo io**.
8. Aprire una conversazione nuova con quel GPT e lasciarla vuota.

### A.1 In aula: primo prompt

**Dire:** "Questo è un GPT normale, di quelli che potete creare voi in dieci
minuti. Ha una sola cosa dentro: il file della tassonomia. Adesso gli do sei
richieste e gli chiedo una tabella."

**Fare:** condividere lo schermo del browser. Incollare nella chat del GPT
esattamente questo, e premere invio.

```
Classifica queste sei richieste e restituisci la tabella.

R001 | email | Buongiorno, vorremmo iscrivere due dipendenti al corso sul nuovo Codice dei contratti del 18 settembre. Potete confermare la disponibilità dei posti e inviarci il modulo? Grazie.

R003 | email | Con riferimento alla fattura n. 2026/311 relativa al corso Bilancio enti locali, segnaliamo che manca il CIG. Senza CIG non possiamo procedere al pagamento.

R004 | email | Salve, il corso Privacy e GDPR di domani mattina è confermato? Non abbiamo ricevuto il link Zoom.

R007 | email | È il terzo sollecito. Ho scritto due volte per l'attestato del corso Bilancio e contabilità degli enti locali e nessuno risponde. Se non ricevo riscontro entro venerdì porto la questione alla direzione.

RE01 | email | Buongiorno ho concluso il corso dei Contratti Pubblici in PromoPa, ho superato il test, ma non mi fa scaricare l'attestato. Potete verificare il problema? L'ufficio personale non mi ha dato risposta, grazie

RE12 | email | Si informa che la casella postale tecnico@comune.t.it è in fase di dismissione. Per contattare l'ufficio Tecnico scrivere a tecnico@comune.it
```

**Mentre elabora, dire:** "Notate che non gli ho detto quali sono le
categorie. Le legge dal file. Se domani aggiungete un corso, cambiate il file,
non questo messaggio."

**Quando risponde, dire:** "Guardate la penultima riga, RE01. È una richiesta
vera arrivata a voi. Il partecipante ha finito il corso, ha passato il test, e
la piattaforma non gli fa scaricare l'attestato. Secondo voi è un problema di
attestato o un problema di piattaforma?"

**Fare:** aspettare. Leggere due o tre risposte dalla chat ad alta voce.

**Poi dire:** "Non c'è una risposta ovvia. Quando ho preparato questo
materiale l'ho etichettata accesso alla piattaforma, il modello dice attestato.
Tenete a mente questa cosa, perché torna fra venti minuti."

**E poi:** "L'ultima riga invece non è una richiesta. È un messaggio automatico
di una casella che viene dismessa. Il modello l'ha smistata comunque, alla
segreteria. Un sistema che smista tutto smista anche il rumore."

### A.2 Secondo prompt: la chat Zoom

**Dire:** "Adesso gli do una cosa più difficile: diciassette righe di chat di
un corso. Dentro ci sono quattro richieste vere e tredici righe di rumore."

**Fare:** incollare esattamente questo.

```
Questa è la chat di un corso su Zoom. Estrai solo le richieste vere, con l'orario e il motivo per cui sono richieste. Poi classificale.

[10:02] Segreteria Promo PA: Buongiorno a tutti, benvenuti al corso Codice dei contratti pubblici.
[10:03] Comune di Pisa - L.R.: buongiorno
[10:03] Provincia - G.M.: buongiorno a tutti
[10:11] Comune di Pisa - L.R.: le slide verranno inviate dopo?
[10:12] Segreteria Promo PA: sì, su Moodle entro domani
[10:25] Unione Valdera - S.T.: non sento bene il docente, si sente solo a me?
[10:25] Provincia - G.M.: io sento bene
[10:26] Unione Valdera - S.T.: ok risolto, era il mio audio
[10:48] Comune di Livorno - A.F.: domanda per il docente: la soglia per l'affidamento diretto vale anche per i servizi di ingegneria?
[10:52] Comune di Pisa - L.R.: mi associo alla domanda di Livorno
[11:30] Segreteria Promo PA: pausa 10 minuti
[11:41] Comune di Lucca - P.D.: scusate, l'attestato viene rilasciato automaticamente o dobbiamo richiederlo?
[11:45] Segreteria Promo PA: lo trovate su Moodle a fine corso
[12:20] Provincia - G.M.: sarebbe utile un corso di approfondimento solo sulla parte esecuzione del contratto
[12:21] Comune di Livorno - A.F.: concordo
[12:29] Comune di Pisa - L.R.: grazie mille, ottimo corso
[12:30] Segreteria Promo PA: grazie a tutti, a presto
```

**Quando risponde, dire, indicando con il puntatore:** "Le dieci e
venticinque, non sento bene, non è stata estratta: alle dieci e ventisei
l'utente scrive che ha risolto. Le dodici e ventinove, grazie mille ottimo
corso, non è stata estratta: è un ringraziamento, non una cosa da fare. Le
dodici e venti invece sì, ed è la più preziosa di tutte, perché è un
partecipante che vi sta dicendo quale corso vendere il mese prossimo."

**Se il modello ne estrae cinque invece di quattro** (capita, di solito
aggiunge la riga delle dieci e venticinque): non nasconderlo. Dire: "Ne ha
prese cinque. La riga dell'audio l'utente stesso dichiara risolta un minuto
dopo. È esattamente il tipo di errore che si scopre solo misurando, e fra
mezz'ora vedremo con quali numeri."

### A.3 Terzo prompt: la bozza

**Fare:** incollare.

```
Scrivi la bozza di risposta per R007.
```

**Quando risponde, dire:** "Guardate le parentesi quadre. Il modello non sa
quando arriverà l'attestato e non se lo inventa: lascia un buco visibile.
Questa è una regola scritta nelle istruzioni, non buona volontà del modello.
Preferiamo un buco che l'operatore riempie in dieci secondi a una data
inventata che ci fa fare una figuraccia."

### A.4 Il cambio di tassonomia, se c'è tempo

**Dire:** "Un'ultima cosa e passiamo al codice."

**Fare:** incollare.

```
Nel file della tassonomia non esiste una categoria per le richieste commerciali: preventivi, sconti, codici MEPA. Fai finta che ci sia, si chiama "commerciale" e la gestisce l'amministrazione. Riclassifica RE01 e le due richieste di acquisto che ti ho dato.
```

**Dire:** "Non ho toccato le istruzioni del GPT. Ho cambiato una voce. Il
comportamento è cambiato. Questo è il punto: il sistema è vostro perché il
file è vostro."

## Parte B. Con il codice (5 minuti)

**Dire, prima di condividere il terminale:** "Adesso la stessa identica logica,
ma in Python, perché è l'unico modo per misurarla. Non serve che seguiate il
codice: guardate solo cosa esce."

**Fare:** condividere lo schermo del terminale.

### B.1 Il backend a regole, per confronto

**Fare:** incollare e premere invio.

```bash
HELPDESK_BACKEND=mock python -m helpdesk_agent.pipeline
```

Esce subito. In fondo compare questo:

```
Valutazione contro le etichette di riferimento:
Richieste valutate: 39
  corso         97.4%
  tipologia     59.0%
  urgenza       61.5%
  operatore     61.5%
  tutti         38.5%
Assegnate automaticamente: 66.7%
```

**Dire:** "Questa non è AI. Sono trenta righe di regole a parole chiave: se
c'è scritto fattura vai in amministrazione. Trentotto virgola cinque per cento
di richieste con tutti e quattro i campi giusti. Tenetelo a mente, perché è il
numero contro cui misureremo."

### B.2 Il modello vero, sulla chat Zoom

**Fare:** incollare e premere invio.

```bash
python -m helpdesk_agent.pipeline --solo-grezzi
```

Impiega circa un minuto. **Non stare in silenzio.** Mentre gira, dire:

"Sta facendo due cose. Prima manda al modello la chat Zoom e il questionario e
si fa dire quali righe sono richieste. Poi classifica quelle che ha trovato.
Le classificazioni le fa in parallelo, sei alla volta, perché sono
indipendenti fra loro: in fila ci metterebbe cinque minuti."

"Il fatto che ci metta un minuto per dieci richieste vi dice anche un'altra
cosa: questo non è un sistema che risponde mentre l'utente aspetta. È un
sistema che gira la notte, o ogni ora, e la mattina la segreteria trova la
coda pronta."

Quando finisce, sullo schermo c'è più o meno questo:

```
Richieste estratte da Zoom e Moodle: 10
  Z-1011   contenuti            -> coordinamento-docenti  [auto]
  Z-1048   contenuti            -> coordinamento-docenti  [auto]
  Z-1141   attestato            -> segreteria-didattica   [auto]
  Z-1220   contenuti            -> coordinamento-docenti  [auto]
  Q02      feedback             -> direzione              [auto]
  ...
```

**Dire:** "Le sigle sono gli orari: Z-1141 è la richiesta delle undici e
quarantuno, quella sull'attestato. Non è un dettaglio estetico: se il codice
non ricostruisse l'identificativo dalla riga di origine, non potremmo più dire
da dove viene una richiesta, e senza quello non si misura niente."

### B.3 Quello che vedrebbe la segreteria

**Fare:** incollare.

```bash
open ../demo/output/coda_per_operatore.md
```

**Dire:** "Questo è il file che la segreteria troverebbe la mattina. Una
sezione per ruolo, dentro le richieste ordinate per urgenza, e accanto a
quelle sotto soglia la scritta DA VERIFICARE. Non è un prodotto, è un file di
testo. Ma è già più di quello che avete adesso."

### B.4 Il momento migliore: una richiesta dettata da loro

**Dire:** "Adesso facciamo una cosa. Scrivetemi in chat una richiesta, come ve
la scriverebbe un vostro utente. Anche brutta, anzi meglio se brutta. La prima
che leggo la do in pasto al sistema."

**Fare:** aspettare venti secondi. Prendere la prima, incollarla in questo
comando fra virgolette doppie:

```bash
python -m helpdesk_agent.una --bozza "QUI IL TESTO CHE HANNO SCRITTO"
```

Attenzione a una cosa sola: **se nel testo ci sono virgolette doppie,
toglierle** prima di incollare, altrimenti il comando si rompe. Gli apostrofi
vanno bene.

Impiega quattordici secondi. Esce così:

```
Backend: openai   soglia: 0.7
------------------------------------------------------------------
corso              nessuno
tipologia          attestato
urgenza            alta
operatore          segreteria-didattica
confidenza         0.86
campo meno sicuro  corso
riassunto          ...
------------------------------------------------------------------
ASSEGNATA in automatico a segreteria-didattica

Bozza di risposta:
...
```

**Dire, leggendo la riga della confidenza:** "Zero virgola ottantasei. La
soglia è zero virgola sette, quindi assegna da solo. Fra dieci minuti vi
mostro perché questo numero, da solo, non basta a proteggervi."

**Se il comando dà errore**, qualunque errore: non provare a ripararlo in
diretta. Dire "me lo guardo dopo" e passare alla slide successiva. Il piano B
è già aperto in una scheda.

## Se la rete cade

Zero drammi, e va detto ad alta voce: "Salta la rete, uso i risultati di una
esecuzione vera di giovedì scorso, che è anche il motivo per cui li ho
congelati nel repository."

Poi aprire `demo/output_esempio/coda_per_operatore.md` e
`demo/output_esempio/valutazione.json` e raccontare quelli. Le slide 47, 57,
58 e 60 mostrano già quegli stessi numeri, quindi il discorso regge intero.

---

# Blocco 1. Riaggancio e tesi (0:00 - 0:10)

## Slide 1. Agenti AI per i processi interni

**Fare:** condividere lo schermo con la slide già aperta. Aspettare che il
contatore dei collegati si fermi.

**Dire:** "Buongiorno. Sono Fabrizio Silvestri, insegno alla Sapienza, e ci
siamo già visti a giugno. Oggi due ore su una cosa diversa: non più l'AI come
strumento personale, ma l'AI dentro un vostro processo."

**Dire, subito dopo:** "Una cosa in dieci secondi, prima di cominciare. Tutte
le fotografie di queste slide sono generate con l'intelligenza artificiale.
Non c'è nessun obbligo che mi imponga di dirvelo. Ve lo dico perché è buona
educazione, ed è l'esempio più corto che ho di cosa vuol dire dichiararlo."

**Note.**
- Non aggiungere altro sulle fotografie: se qualcuno chiede, si riprende nel blocco 4.
- Se qualcuno arriva tardi, non ricominciare.

## Slide 2. Sezione 1

**Dire:** "Primo blocco, dieci minuti. Riprendiamo il filo da giugno e vi dico
qual è la tesi della giornata, così sapete dove andiamo a parare."

## Slide 3. Da giugno a oggi

**Dire:** "A giugno abbiamo visto ChatGPT come un collega: gli scrivete, vi
risponde, gli date dei documenti. Oggi cambiamo scala. Non più una persona che
usa uno strumento, ma un processo che ne contiene uno."

**Dire, sul terzo bullet:** "Il caso di studio non me lo sono inventato: è il
vostro helpdesk formazione, con i vostri numeri e, da metà mattina, con dodici
richieste vere che mi avete mandato."

**Fare:** chiedere in chat. "Prima domanda, una parola a testa in chat: da
giugno, chi ha provato a creare un Progetto o un GPT personalizzato?"

**Note.**
- Due minuti, non di più. Da remoto conviene la chat al giro di tavolo.
- ChatGPT Business è già in uso in Fondazione: tutto quello che vediamo oggi si può provare lì senza comprare niente.

## Slide 4. Che cosa sapete già fare

**Dire:** "Do per acquisite tre cose. Se una di queste vi manca, mettetevi in
coppia con qualcuno che ce l'ha, perché oggi partiamo da qui."

**Dire, sul terzo bullet:** "La terza è la più importante e la meno praticata:
accorgersi quando il modello sta inventando. Torna alla fine, quando parliamo
di allucinazioni."

## Slide 5. La scaletta di oggi

**Dire:** "Sei blocchi, due ore. Il primo terzo è vocabolario, il secondo è il
vostro caso, il terzo è cosa non funziona e cosa fare lunedì."

**Dire, indicando il blocco 6:** "L'ultima mezz'ora è vostra. Non farò lezione:
lavorate voi su un processo della Fondazione."

**Dire:** "Ultima cosa sul metodo. Le slide sono cento, ma molte durano dieci
secondi perché sono immagini. Interrompete quando volete: da remoto è più
difficile, quindi scrivete in chat anche solo un punto interrogativo e mi
fermo."

## Slide 6. Chatbot, workflow, agente

**Dire:** "Tre parole che nelle offerte vengono usate come sinonimi e non lo
sono. Da sinistra a destra cresce l'autonomia e cala il controllo."

**Dire:** "Un chatbot risponde e finisce lì. Un workflow è una sequenza di
passi che decidete voi, e l'AI sta dentro uno o due di quei passi. Un agente
decide da solo quali passi fare e quando fermarsi."

**Dire, con calma:** "Quasi tutto quello che vi verrà proposto come agente è,
o dovrebbe essere, un workflow. Non è una critica ai fornitori: è che
l'autonomia si paga in prevedibilità, e voi la prevedibilità la volete."

## Slide 7. L'agente autonomo che vi immaginate

**Dire:** "Questo è l'agente autonomo." Pausa di due secondi. "Decide da solo,
e non arriva alla tastiera."

**Note.**
- Slide per ridere. Dieci secondi, non spiegarla.
- Il punto serio: quando un fornitore dice agente autonomo, chiedere cosa sa fare da solo davvero.

## Slide 8. I tre tipi, con un esempio ciascuno

**Dire:** "Un esempio per ciascuno, presi da casa vostra."

**[clic]** "Chatbot: chiedete a ChatGPT come si scrive una convocazione. Vi
risponde. Fine."

**[clic]** "Workflow: arriva una richiesta, il modello la classifica, una
regola la manda all'ufficio giusto, una persona rilegge e invia. Quattro passi,
di cui uno solo con AI dentro. È quello che costruiamo oggi."

**[clic]** "Agente: gli dite sistema l'helpdesk e decide lui i passi. Non è
fantascienza, si può fare. Oggi non lo vogliamo, e alla fine capirete perché."

## Slide 9. La tesi in tre righe

**Dire:** "Se oggi vi addormentate, svegliatevi qui. Tre righe."

**[clic]** "Prima si scompone il processo, poi si decide cosa automatizzare.
Non il contrario."

**[clic]** "Dove serve giudizio o dove c'è una responsabilità, resta una
persona. Non per prudenza: per progetto."

**[clic]** "Si misura prima di automatizzare, e si rimisura dopo. Altrimenti
funziona bene è un'opinione."

**Dire:** "Queste tre righe tornano alla fine, girate al contrario, come i tre
errori da evitare."

---

# Blocco 2. Anatomia di un sistema agentico (0:10 - 0:30)

## Slide 10. Sezione 2

**Dire:** "Venti minuti di vocabolario. Non per farvi diventare tecnici: per
farvi capire quando qualcuno vi sta vendendo un agente e a voi serve una
regola."

## Slide 11. I cinque pezzi 1/2

**Dire:** "Qualunque sistema di questo tipo ha cinque pezzi. Al centro c'è il
modello, e le quattro frecce puntano tutte verso di lui: gli altri quattro
pezzi servono il modello, non il contrario."

**Dire:** "Modello: legge testo e produce testo, o meglio produce dati.
Strumenti: la casella, Zoom, Moodle. Memoria: la tassonomia e le regole, cioè
un file che scrivete voi."

## Slide 12. I cinque pezzi 2/2

**Dire:** "Gli altri due. Il ciclo di azione: leggi, decidi, agisci, verifica.
E il punto di controllo umano."

**Dire, scandendo:** "Un sistema senza punto di controllo non è coraggioso, è
incompleto. Se in un'offerta non riuscite a trovarlo, non c'è."

## Slide 13. Il modello: cosa sa e cosa non sa

**Dire:** "Il modello sa la lingua e sa che forma ha una determina. Non sa i
vostri corsi, non sa chi è la vostra segreteria didattica, non sa che il corso
del 18 settembre è pieno."

**Dire:** "E qui c'è la cosa che sorprende tutti: non se lo ricorda. Ogni volta
che gli parlate, glielo dovete ridire. Sembra un difetto, in realtà è la
ragione per cui il sistema resta vostro: quello che sa, glielo date voi, in un
file che potete cambiare."

## Slide 14. Gli strumenti: il modello non possiede niente

**Dire:** "Il modello non ha una casella di posta. Legge la vostra se qualcuno
gliela collega, e smette di leggerla nel minuto in cui gli togliete il
permesso."

**Fare:** chiedere in chat. "Domanda: quali permessi dareste, e quali no?"

**Dire, dopo le risposte:** "La risposta che arriva quasi sempre è: leggere sì,
scrivere forse, inviare mai. È esattamente il disegno che vi propongo."

## Slide 15. La memoria: la tassonomia siete voi

**Dire:** "Quando si parla di memoria si pensa al fatto che si ricordi la
conversazione. Non è quella che conta. La memoria che conta è un file, scritto
da voi, con dentro le vostre categorie e le vostre regole."

**Dire:** "Cambiare un corso vuol dire cambiare una riga di quel file. Non
riscrivere il sistema, non richiamare il fornitore, non aprire un ticket."

## Slide 16. Il ciclo di azione

**Dire:** "Quattro passi in cerchio: leggi, decidi, agisci, verifica. Poi da
capo."

**Dire:** "Il quarto è quello che sparisce dalle offerte. Se togliete verifica,
non avete più un ciclo: avete una freccia dritta che va da qualche parte e non
torna."

## Slide 17. Il punto di controllo umano

**Dire:** "Tre forme: una soglia di confidenza, una coda da verificare, l'invio
manuale. Si progettano prima, non si aggiungono dopo che è successo qualcosa."

**Dire:** "Segnatevi il terzo bullet, perché è una promessa che mantengo fra
mezz'ora: la soglia di confidenza, da sola, non basta. Ve lo dimostro con i
numeri di questo repository."

## Slide 18. Pattern utili 1/2

**Dire:** "Due schemi ricorrenti, e sono quelli che coprono il vostro caso
quasi per intero."

**Dire:** "Routing: entra una richiesta, esce un destinatario. Se il sistema
non è sicuro, invece del destinatario esce una coda umana."

**Dire:** "Estrazione strutturata: entra testo libero, escono campi fissi. Chi,
cosa, quando."

## Slide 19. Pattern utili 2/2

**Dire:** "Altri due, che vi servono solo per riconoscerli in un'offerta.
Orchestratore e worker: un modello spezza un compito lungo e altri lo
eseguono. Valutatore: un secondo passaggio che controlla il primo."

**Dire, rallentando:** "La regola d'oro è la riga in fondo. Compito piccolo,
formato di uscita rigido, una persona dove costa sbagliare. Se un'offerta
rispetta queste tre cose, potete anche non capire come è fatta dentro."

## Slide 20. Parole da riconoscere in un'offerta 1/3

**Dire:** "Tre slide di glossario. Non per sapere cosa vuol dire: per sapere
quando qualcuno le sta usando a sproposito."

**Dire:** "RAG: il modello cerca nei vostri documenti prima di rispondere.
Utile, non magico, e non risolve il problema di documenti scritti male."

**Dire:** "Fine tuning: si riaddestra il modello sui vostri dati. Caro, lento,
e per trecento richieste al mese quasi certamente inutile. Se ve lo propongono
per questo caso, è un campanello."

## Slide 21. Parole da riconoscere in un'offerta 2/3

**Dire:** "Output strutturato: il modello restituisce campi fissi invece di
prosa. Chiedetelo sempre, perché è la differenza fra una cosa misurabile e un
tema di italiano."

**Dire:** "Guardrail: controlli che bloccano le uscite fuori regola. Fateveli
mostrare sullo schermo, non descrivere a parole."

**Dire:** "Human in the loop. Se un fornitore ve la dice senza aggiungere in
quale passo, è una formula vuota. Chiedete: in quale schermata, e cosa vede
quella persona."

## Slide 22. Parole da riconoscere in un'offerta 3/3

**Dire:** "Allucinazione: il modello inventa con sicurezza. Non si elimina, si
contiene. Chi vi dice che il suo sistema non allucina o non sa di cosa parla o
spera che non ve ne accorgiate."

**Dire:** "Token: è l'unità con cui si paga, e nessuno sa stimarli a occhio.
La domanda giusta non è quanto costa un token, è quanto costano mille
richieste come le nostre."

## Slide 23. Quando NON usare un agente

**Dire:** "Tre casi in cui la risposta è no, e ve li dico io che sono venuto a
parlarvi di AI."

**[clic]** "Se la regola si scrive in un se allora, è una regola. Assegna
all'amministrazione tutto quello che contiene la parola fattura: quella è una
riga di codice, non serve un modello."

**[clic]** "Se un errore costa più del tempo che risparmiate, serve una
persona."

**[clic]** "Se non avete dati per misurarlo, non saprete mai se funziona.
Prima i dati."

## Slide 24. Tre domande da fare a un fornitore

**Dire:** "Chiudo il blocco con tre domande. Si fanno in due minuti e separano
un fornitore serio da un venditore."

**[clic]** "Su quali dati avete misurato l'accuratezza, e posso vedere il
campione? Se la risposta è un numero senza campione, il numero non vale."

**[clic]** "In quale passo esatto interviene una persona, e cosa vede sullo
schermo?"

**[clic]** "Se cambio la tassonomia, cosa devo toccare, quanto costa e chi lo
fa? Se la risposta è apriamo un ticket, avete comprato un vestito che non
potete più modificare."

**Fare:** incollare le tre domande in chat, così le hanno scritte.

---

# Blocco 3. Il caso helpdesk formazione (0:30 - 1:00)

Trenta minuti, la demo dentro. La demo ha la sua sezione dedicata più sopra:
qui ci sono le slide che la circondano.

## Slide 25. Sezione 3

**Dire:** "Mezz'ora sul vostro caso. Nella prima metà scomponiamo, nella
seconda ve lo faccio vedere che gira."

## Slide 26. I vostri numeri

**Dire:** "Tre numeri, che mi avete dato voi l'otto settembre. Circa
trecento richieste al mese. Cinque caselle diverse. Zero strumenti di
tracciamento."

**Dire:** "Trecento al mese sono quindici al giorno lavorativo. Lo dico subito
perché sgonfia l'ansia: nessuno qui ha un problema di scala. Avete un problema
di ordine."

## Slide 27. Quindici richieste al giorno

**Dire:** "Non è un volume da piattaforma. È un volume da tabella e da regole."

Dieci secondi, poi avanti.

## Slide 28. Da dove arrivano le richieste

**Dire:** "Cinque imbuti, un barattolo. Tre dei cinque canali oggi arrivano a
qualcuno: le caselle, i moduli del sito, i messaggi Moodle. Due si perdono per
strada: i questionari e le chat Zoom."

**Dire:** "E sono proprio i due che si perdono quelli che contengono i
suggerimenti su quali corsi fare."

## Slide 29. Cinque caselle

**Dire:** "Cinque caselle e-mail sono cinque telefoni sulla stessa scrivania.
Il problema non è che siano cinque: è che nessuna sa cosa succede nelle altre
quattro."

## Slide 30. Il sistema di tracciamento attuale

**Dire, con leggerezza:** "Questo funziona benissimo. Finché la persona che ha
scritto i foglietti è in ufficio."

**Note.**
- Detto senza colpevolizzare nessuno: è così in quasi tutte le organizzazioni sotto una certa dimensione.

## Slide 31. Cosa si perde per strada

**Dire:** "Le chat Zoom nessuno le rilegge. I questionari: si contano le
stelline e non si leggono le frasi."

**Dire, sul terzo bullet:** "Le telefonate oggi sono fuori portata, ma vi lascio
un compito che costa zero: un foglio accanto al telefono per quattro settimane,
una riga per chiamata. Spesso cambia le priorità di tutto il progetto."

## Slide 32. Le quattro esigenze

**Dire:** "Dalla vostra e-mail ho ricavato quattro esigenze. Guardate la
colonna in mezzo: solo due su quattro hanno bisogno di un modello. Le altre
due sono integrazione e organizzazione."

**Dire:** "E l'ordine che consiglio è controintuitivo: prima la uno, la tre e
la quattro, e la due per ultima. La due, cioè Zoom e Moodle, è la più
affascinante e la meno urgente."

## Slide 33. Esigenza 1: repository unico

**Dire:** "Un contenitore solo, più i connettori che ci portano dentro le cose.
Non è AI, ed è la cosa che vi cambierà di più la giornata."

**Dire:** "Va bene un foglio condiviso. Va bene un ticketing gratuito. Purché
sia uno solo, e purché da lì in poi ogni richiesta abbia un identificativo, uno
stato e un responsabile."

## Slide 34. Il contenitore che oggi non c'è

**Dire:** "Ecco perché la uno viene prima della due. Se estraete richieste
dalle chat Zoom e non avete dove metterle, avete solo creato lavoro."

## Slide 35. Come si costruisce il contenitore

**Dire:** "Tecnicamente è un pomeriggio. I connettori dalle caselle si fanno a
basso codice, senza scrivere una riga."

**Dire, rallentando:** "La regola vera è l'ultima, ed è organizzativa: nessuno
risponde più direttamente dalla propria casella. Quella non costa niente in
tecnologia ed è il punto in cui questi progetti falliscono."

## Slide 36. L'integrazione è idraulica, non intelligenza

**Dire:** "Spostare dati da un posto a un altro senza interpretarli non
richiede un modello. È noioso, è la maggior parte del lavoro, e non lo mette
nessuno nelle presentazioni."

**Dire:** "Regola pratica: se un'offerta è tutta AI e niente integrazione,
manca il settanta per cento del progetto."

## Slide 37. Esigenza 2: Zoom e Moodle

**Dire:** "Questa è la chat vera di un vostro corso, diciassette righe. Dentro
ci sono quattro richieste."

**Fare:** con il puntatore, indicare le quattro righe mentre le si legge.

**Dire:** "Le dieci e undici: le slide verranno inviate dopo. Le dieci e
quarantotto: domanda per il docente. Le undici e quarantuno: l'attestato viene
rilasciato automaticamente. Le dodici e venti: sarebbe utile un corso
sull'esecuzione del contratto."

**Dire:** "E adesso guardate le dieci e venticinque: non sento bene. Sembra una
richiesta, non lo è, perché un minuto dopo la stessa persona scrive ok
risolto. E le dodici e ventinove, grazie mille ottimo corso, non è un feedback
azionabile: è educazione."

## Slide 38. Esigenza 2: cosa esce dall'estrazione

**Dire:** "Questo è quello che esce. Notate il campo motivazione: non serve al
modello, serve a voi, per controllare a campione senza rileggere tutto."

**Dire:** "Il terzo bullet nasce da un errore vero che ho fatto io. La prima
volta ho lasciato che fosse il modello a decidere l'identificativo, e lui ci
metteva dentro anche il nome del mittente. Risultato: quattro richieste su
quaranta non erano più rintracciabili e la valutazione non tornava. Adesso
l'orario lo estrae il codice con una regola fissa."

## Slide 39. Esigenza 3: classificazione 1/2

**Dire:** "Questa è la tassonomia, ed è un file di testo di quaranta righe. Lo
scrivete voi, non il fornitore."

**Dire:** "Guardate la parte in fondo: gli operatori sono ruoli. C'è scritto
segreteria didattica, non il nome di chi ci lavora. E c'è la soglia di
confidenza, zero virgola sette, che è un numero che decidete voi."

## Slide 40. Esigenza 3: classificazione 2/2

**Dire:** "E questo è quello che il modello deve restituire. Non un tema:
questo oggetto, con questi campi, o un errore."

**Dire:** "Due campi meritano attenzione. La confidenza, che decide se assegnare
o fermarsi. E il campo meno sicuro, in cui il modello dichiara dove è più
debole: in questo caso l'urgenza. Fra venti minuti scoprirete che aveva
ragione."

## Slide 41. La tassonomia si scrive così

**Dire:** "Tre regole per scriverla. Ogni voce ha una descrizione, perché
serve al modello quanto alla persona nuova che entra in segreteria."

**Dire:** "Le voci sono poche e non si sovrappongono. Se due voci litigano fra
loro, il modello sbaglia, e non è colpa sua."

**Dire:** "E c'è sempre una voce altro. Non è una discarica, è un termometro:
se supera il dieci per cento vi manca una categoria."

## Slide 42. Gli operatori sono ruoli, non persone

**Dire:** "Cinque sedie uguali. Nel file c'è il ruolo, non il nome. Se qualcuno
cambia mansione o va in maternità, la tassonomia non invecchia."

**Dire:** "C'è anche un motivo di riservatezza: in quel file non finiscono nomi
di dipendenti."

## Slide 43. Esigenza 4: tracciamento e follow-up

**Dire:** "Stati e scadenze sono deterministici: nuova, presa in carico, in
attesa, chiusa. Qui non c'è nessuna AI, e infatti non serve."

**Dire:** "L'unica cosa che fa l'AI è scrivere la bozza. L'operatore la rilegge
e la invia. Sempre."

## Slide 44. Gli stati di una richiesta

**Dire:** "Quattro stati, tre frecce avanti e una indietro. Da in attesa utente
si torna a presa in carico, perché l'utente risponde."

**Dire:** "Questa è la parte che si fa in mezza giornata con un foglio
condiviso, ed è quella che dà il sollievo più immediato alla segreteria."

## Slide 45. L'architettura, tutta insieme

**Dire:** "Tutto insieme. Sette passi. Contate le targhette accese: tre."

**Dire, scandendo:** "Tre passi su sette hanno un modello dentro. Gli altri
quattro sono idraulica: spostare dati, applicare una regola, far rileggere a
una persona. Se vi ricordate una sola slide di oggi, ricordatevi questa."

**Dire, indicando la freccia che scende:** "E questa è la diramazione: quando
la confidenza è sotto soglia, il sistema non assegna e la richiesta va a una
persona."

## Slide 46. Demo dal vivo: cosa vedrete

**Dire:** "Adesso ve lo faccio vedere che gira. Tre cose: un GPT
personalizzato che potete rifare voi stasera, la stessa logica in Python
perché è l'unico modo per misurarla, e la chat Zoom che diventa righe di
tabella."

**Fare:** da qui in avanti seguire la sezione "La demo, parola per parola".
Tornare alle slide alla 47.

## Slide 47. Demo: il risultato

**Dire:** "Questo è un estratto dell'esecuzione vera di giovedì scorso. Dieci
righe su quaranta. Le righe gialle sono urgenza alta."

## Slide 48. Demo: le tre righe da guardare

**[clic]** "R007: reclamo con sollecito. Il tono prevale sull'oggetto. L'oggetto
è un attestato, ma il modo in cui è scritto dice reclamo, e va alla direzione."

**[clic]** "RE01: quella di prima, l'attestato bloccato dalla piattaforma. Due
categorie plausibili, nessuna ovvia. Questa è la riga che vale la lezione."

**[clic]** "RE05: non è nemmeno una domanda. È la notifica automatica di un
ordine MEPA."

## Slide 49. Demo: una bozza di risposta (R007)

**Dire:** "La bozza per il reclamo. Leggete la prima frase: riconosce il
disagio in una riga, senza giustificazioni. È una regola scritta nel prompt."

**Dire:** "E poi le due parentesi quadre."

## Slide 50. Demo: perché ci sono i segnaposto

**Dire:** "Una data inventata è un danno. Un buco visibile è dieci secondi di
lavoro per l'operatore."

**Dire:** "La risposta pericolosa non è quella sbagliata: è quella verosimile.
I segnaposto servono a rendere visibile l'ignoranza del sistema."

## Slide 51. Dodici richieste vere

**Dire, cambiando tono:** "Adesso cambio registro. Fino a qui i dati erano
inventati da me. Da qui in poi sono i vostri: dodici richieste arrivate
davvero alla Fondazione, che mi avete mandato anonimizzate."

**Note.**
- Dirlo esplicitamente: cambia l'attenzione della sala.
- Il documento era già anonimizzato bene, nomi e codici sostituiti da X. Vale la pena dirlo.

## Slide 52. Cosa ci hanno insegnato le dodici 1/3

**[clic]** "Dieci su dodici hanno corso nessuno."

**[clic]** "Lavoro agile, cyber security, OIV, valutazione della performance,
società partecipate. Nessuno di questi era nella tassonomia che avevo scritto
io."

**[clic]** "Non è un errore del modello. È la tassonomia che va riscritta sul
vostro catalogo vero. Questo è il risultato più utile della giornata, e non era
previsto."

## Slide 53. Cosa ci hanno insegnato le dodici 2/3

**[clic]** "Tre su dodici sono richieste commerciali: preventivi, sconti,
codici MEPA."

**[clic]** "Nella tassonomia non c'è una voce per il commerciale, e le ho messe
sotto fatturazione."

**[clic]** "È l'approssimazione migliore disponibile, ed è comunque sbagliata."

**Fare:** chiedere. "Domanda vera: chi risponde oggi a una richiesta di sconto?"

**Dire, dopo le risposte:** "Se la risposta è dipende, avete appena trovato la
prossima voce della vostra tassonomia."

## Slide 54. Cosa ci hanno insegnato le dodici 3/3

**[clic]** "Una su dodici non è una richiesta. È l'avviso automatico di una
casella che viene dismessa."

**[clic]** "Il modello l'ha classificata come informazioni e l'ha mandata alla
segreteria."

**[clic]** "Un sistema che smista tutto smista anche il rumore. Serve una voce
per buttare via, e serve qualcuno che possa dire questa non è una richiesta."

---

# Blocco 4. Limiti e rischi (1:00 - 1:15)

Quindici minuti. È il blocco che serve a evitare che qualcuno compri qualcosa a
ottobre sull'onda dell'entusiasmo. Le slide 57 e 58 sono le più importanti
della giornata.

## Slide 55. Sezione 4

**Dire:** "Quindici minuti su cosa non funziona. Senza giri di parole, perché
è la parte che vi serve di più."

## Slide 56. L'accuratezza si misura, non si stima

**Dire:** "Per sapere se un sistema del genere funziona serve un campione
etichettato a mano. Cento, duecento richieste storiche, classificate da due
persone in parallelo, poi confrontate."

**Dire:** "E qui c'è la frase che vi porterete a casa: dove le due persone non
concordano, il problema non è il modello, è la tassonomia."

**Dire:** "Quello che vi mostro adesso non è un caso di scuola. È misurato su
questo repository, giovedì scorso, su quaranta richieste: diciannove inventate
da me, dodici vostre, nove estratte dalle chat."

## Slide 57. I numeri di questa esecuzione

**Dire:** "Cinque barre. Il corso al cento per cento, tipologia e operatore
all'ottantacinque, l'urgenza al settantadue e mezzo."

**Dire, onestamente:** "Il cento per cento sul corso è meno bello di quanto
sembri: dieci richieste su dodici avevano corso nessuno, ed è facile
indovinare quando la risposta giusta è nessuno."

**Dire, indicando la barra in fondo:** "Ma la barra che conta è l'ultima.
Sessanta per cento di richieste con tutti e quattro i campi giusti. Vuol dire
che quattro su dieci hanno almeno un campo sbagliato."

**Dire:** "Per confronto, le regole a parole chiave che avete visto in demo
stavano al trentotto e mezzo. Il modello raddoppia, e non basta ancora."

## Slide 58. Il modello è sicuro anche quando sbaglia

Questa è la slide più importante. **Fermarsi. Non parlare per tre secondi.**

**Dire:** "Guardate questo grafico. In alto le richieste classificate bene, in
basso quelle con almeno un campo sbagliato. Sull'asse orizzontale c'è la
confidenza che il modello si è dato da solo."

**Dire, indicando la linea nera:** "Questa è la soglia: zero virgola sette.
Sotto quella linea il sistema non assegna e manda la richiesta a una persona."

**Dire, con calma:** "Non c'è niente a sinistra della linea. Nessuna richiesta,
su quaranta, è mai scesa sotto la soglia. La confidenza più bassa dichiarata è
stata zero virgola settantacinque."

**Dire:** "Quindi la coda umana non si è mai riempita. Tutte e quaranta sono
state assegnate in automatico, comprese le sedici sbagliate."

**Dire:** "Il punto di controllo che avevo progettato con tanta cura, da solo,
non ha fermato niente."

## Slide 59. Cosa dice quel grafico

**[clic]** "La confidenza dichiarata non è una probabilità. È un numero che il
modello sceglie, e lo sceglie ottimista."

**[clic]** "Le crocette rosse stanno a destra della soglia esattamente quanto i
pallini blu. Non sono separabili."

**[clic]** "Quindi la coda umana va tarata sui dati, non sul numero che il
modello si autoassegna."

**Dire:** "Come si tara davvero: prendete il campione etichettato, ordinate per
confidenza, e guardate a che punto gli errori si diradano. Se non si diradano
mai, la confidenza non serve e il controllo deve essere un altro, per esempio
tutte le richieste di un certo tipo passano da una persona."

## Slide 60. Dove si concentrano gli errori

**Dire:** "Undici errori su quaranta sul campo urgenza. Sei su tipologia, sei
su operatore, zero sul corso."

**Dire:** "L'urgenza è il campo più soggettivo, ed è quello sbagliato di più.
Non è un caso."

## Slide 61. Urgenza: perché è il campo peggiore

**[clic]** "La regola che ho scritto io dice: urgenza alta solo se c'è un
vincolo di tempo esplicito o un blocco di accesso."

**[clic]** "Ma avrei urgentemente bisogno è un vincolo esplicito, o è solo un
tono?"

**[clic]** "Finché non lo decidete voi, decide il modello, e decide ogni volta
in modo diverso."

**Dire:** "C'è una richiesta vera, RE10, che dice proprio avrei urgentemente
bisogno. Io l'ho etichettata alta, il modello media. Nessuno dei due ha torto:
manca la regola."

## Slide 62. Quando sbaglia il modello e quando la tassonomia

**Dire:** "Questa è la diagnosi più utile che vi portate a casa, ed è un bivio."

**[clic]** "Se due persone della vostra segreteria darebbero risposte diverse,
non è colpa del modello. È la tassonomia che è ambigua."

**[clic]** "Se tutti darebbero la stessa risposta e il modello no, allora sì, è
colpa del modello."

**[clic]** "Il test costa venti minuti su venti richieste, e si fa prima di
comprare qualsiasi cosa."

**Fare:** scriverla in chat, così resta.

## Slide 63. La coda umana, in pratica

**Dire:** "Tre cose sulla coda, perché è l'unica difesa che vi resta."

**Dire:** "Qualcuno la apre ogni mattina, oppure non è un controllo: è un
secondo arretrato."

**Dire, sul secondo bullet:** "E c'è un vantaggio che nessuno sfrutta: ogni
richiesta che una persona rivede è un'etichetta gratis. Rientra nel campione e
migliora la misura. La coda è una macchina che produce dati mentre lavora."

## Slide 64. Cosa può andare storto

**Dire:** "Tre modi di fallire, in ordine di probabilità crescente."

**Dire:** "Il modello cambia versione e i numeri si spostano senza che nessuno
se ne accorga. Un caso nuovo entra in una categoria vecchia perché non ce n'è
una giusta."

**Dire:** "E il terzo, che è il più comune e il meno raccontato: la coda umana
si riempie, nessuno la guarda, e diventa il posto dove le richieste vanno a
morire."

## Slide 65. Da qui in poi non parlo io

**Fare:** rallentare. Guardare la telecamera, non lo schermo.

**Dire:** "Trenta secondi di premessa, e servono a voi quanto a me."

**[clic]** "Sono un informatico, non un avvocato. Quello che segue è contesto,
non un parere."

**[clic]** "Nessuna slide di oggi vi dice se una norma si applica al vostro
caso. Quella è una qualificazione giuridica e la fa un giurista, per iscritto."

**[clic]** "Quello che posso darvi sono le domande giuste e dove andare a
cercare."

**Note.**
- Se in aula arriva "quindi possiamo farlo?", la risposta è sempre: è esattamente la domanda da mettere per iscritto a chi vi segue sul legale.
- Non lasciarsi tirare dentro. Vale anche se insistono.

## Slide 66. Dati personali: quello che riguarda il progetto

**Dire:** "Questa slide parla di progettazione, non di conformità."

**Dire:** "Le richieste contengono nomi, enti, e a volte situazioni personali:
una malattia, un contenzioso."

**Dire, sul secondo bullet:** "E c'è un fatto tecnico da mettere sul tavolo: il
testo di una richiesta esce dalla Fondazione e arriva a un fornitore esterno.
È una scelta, si può fare o non fare, ma va decisa da qualcuno."

**Dire:** "Sul terzo: al modello passiamo solo il testo della singola
richiesta. Non lo storico del mittente, non le altre richieste, non archivi.
Questa è minimizzazione, ed è una scelta di progetto che è già dentro il
codice."

## Slide 67. Chi risponde delle decisioni sui dati

**Dire:** "Prima della tecnologia serve una persona che decida se quel testo
può uscire. Se oggi quella casella è vuota, riempirla è il passo zero."

**Dire:** "Chi debba riempirla, e con quale titolo formale, non lo decido io in
una slide."

## Slide 68. Il perimetro, senza conclusioni

**Dire:** "Tre testi di cui sentirete parlare: l'AI Act europeo, la legge
italiana sull'intelligenza artificiale, le linee guida AgID."

**Dire:** "Nel 2026 le date si sono mosse più di una volta. Qualunque cosa vi
dica oggi va riverificata sul testo ufficiale, e se leggete un articolo di
giornale del 2025 le scadenze che riporta sono probabilmente vecchie."

**Dire:** "Nessuno di questi testi nomina l'helpdesk di una fondazione
formativa. La qualificazione la fa un giurista."

**Note.**
- Non leggere numeri di articolo dalla slide. Non ce ne sono, ed è voluto.
- Se li chiedono: stanno in docs/domande_legali.md con i link e la data di consultazione.

## Slide 69. Le sei domande da mettere per iscritto 1/2

**Dire:** "Sei domande. Mandatele per e-mail a chi le deve firmare, perché una
domanda scritta produce una risposta scritta, e una risposta scritta protegge
chi la riceve."

**[clic]** "Il sistema che vogliamo costruire rientra fra quelli soggetti a
obblighi rafforzati, e su quale base?"

**[clic]** "Dobbiamo dire a chi ci scrive che una parte del processo usa AI? In
quale momento e con quali parole?"

**[clic]** "Con quale base giuridica trattiamo il testo delle richieste, e dove
va scritta?"

## Slide 70. Le sei domande da mettere per iscritto 2/2

**[clic]** "Il fornitore del modello che ruolo assume rispetto ai nostri dati, e
cosa dobbiamo firmare con lui?"

**[clic]** "Serve una valutazione d'impatto prima di partire? Se sì, chi la
redige e chi la firma?"

**[clic]** "E l'ultima, che è la più operativa: ogni umano che togliete dal
ciclo allunga questa lista. Cosa cambierebbe se la risposta partisse da sola?"

**Dire:** "Ecco perché l'invio umano non è solo una scelta di qualità. È anche
quello che tiene corta questa lista."

## Slide 71. Quanto costa davvero

**Dire:** "Le chiamate al modello, su questi volumi, sono la voce più piccola
del conto. Non ve la do in euro perché cambia ogni pochi mesi e non voglio
darvi un numero che fra tre mesi è falso."

**Dire:** "Il costo vero è la persona che ogni trimestre guarda gli errori e
aggiorna il file. Quella non è una licenza, è tempo di qualcuno che avete già."

## Slide 72. Manutenzione

**Dire:** "La pianta secca accanto alla scrivania ordinata: è esattamente cosa
succede a una tassonomia che non è di nessuno."

**Dire:** "Tre regole. Qualcuno la possiede. A ogni cambio di versione del
modello si rimisura sul campione. E se la coda umana supera il trenta per
cento, si rivede la tassonomia, non il modello."

---

# Blocco 5. Dal caso d'uso al pilota (1:15 - 1:30)

Quindici minuti. Da qui in poi si parla solo di cose da fare lunedì.

## Slide 73. Sezione 5

**Dire:** "Quindici minuti su come si parte davvero. Quattro passi, tre mesi,
e la possibilità di fermarsi."

## Slide 74. Passo 1: audit del flusso attuale

**Dire:** "Una o due settimane. Contare le richieste per canale per quattro
settimane, telefonate comprese. Cronometrare quanto passa dalla ricezione alla
prima risposta."

**Dire:** "Costo: un foglio e la costanza di compilarlo. Nessuna tecnologia. E
senza questi numeri, fra sei mesi non saprete dire se è migliorato."

## Slide 75. Passo 2: tassonomia e dati etichettati

**Dire:** "Due settimane, ed è il passo che tutti vogliono saltare. È anche
quello che decide se il resto funziona."

**Dire:** "Scrivere il file con i corsi veri, non quelli che ho inventato io.
Poi etichettare cento, duecento richieste storiche, due persone in parallelo, e
dove non concordano si riscrive la voce."

**Dire:** "Oggi ne abbiamo etichettate quaranta e già si vede dove la
tassonomia scricchiola. Con duecento lo saprete con precisione."

## Slide 76. Passo 3: prototipo a basso codice

**Dire:** "Due-quattro settimane. Contenitore unico, connettori, classificatore,
coda da verificare."

**Dire:** "E un GPT personalizzato basta per cominciare. Il codice serve quando
volete misurare sul serio, non prima."

**Dire, fermandosi:** "L'invio resta umano per tutto il pilota. Senza
eccezioni, nemmeno per le richieste facili."

## Slide 77. Passo 4: misurare un mese, poi decidere

**Dire:** "Un mese con le stesse metriche del passo uno, sugli stessi canali."

**Dire:** "Tre esiti possibili: estendere, correggere, fermare. Tutti e tre
legittimi. La decisione la prende la direzione, con i numeri davanti."

## Slide 78. Chi fa cosa

**Dire:** "Quattro righe. Guardate cosa non c'è: non c'è nessuna riga che dice
consulente esterno."

**Dire:** "Se scoprite che per il passo tre non avete nessuno in Fondazione, è
un'informazione preziosa: comprate quel pezzo lì, non tutto il progetto."

## Slide 79. Il calendario

**Dire:** "Tre mesi dall'inizio alla decisione, ed è realistico solo se nessuno
ci lavora a tempo pieno, che è la vostra situazione."

**Dire:** "I passi si sovrappongono poco, ed è voluto. Comprimere il secondo è
l'errore classico."

## Slide 80. Metriche decise prima di partire

**Dire:** "Tre metriche, e vanno fissate prima. Se le fissate dopo aver visto i
risultati, deciderete che vanno bene comunque."

**Dire, sul terzo bullet:** "Notate come è scritto il terzo: non solo quante
richieste finiscono in coda umana, ma quante di quelle vengono davvero riviste.
Nasce dall'errore che abbiamo visto prima."

## Slide 81. Le tre soglie, spiegate

**[clic]** "Sotto l'ottanta per cento su tipologia e operatore il sistema vi fa
perdere tempo invece di darvene. Oggi siamo all'ottantacinque, con quaranta
richieste."

**[clic]** "Sopra il trenta per cento di coda umana la tassonomia è ambigua.
Non è il modello che è scarso."

**[clic]** "E se il tempo alla prima risposta non scende, il collo di bottiglia
era altrove, e l'avete scoperto spendendo poco."

## Slide 82. Strumenti a basso codice

**Dire:** "ChatGPT Business ce l'avete già. I connettori si fanno con Make,
Zapier, n8n, o con le automazioni di Microsoft 365 e Google Workspace che già
pagate."

**Dire:** "Il criterio non è quale sia il migliore. È quale sa già usare
qualcuno in Fondazione."

## Slide 83. Il report che nessuno legge

**Dire:** "Una metrica che non cambia una decisione è carta."

**Dire:** "Regola pratica: per ogni numero che decidete di misurare, dite in
anticipo quale decisione cambierebbe. Se non ce n'è una, non misuratelo."

## Slide 84. Quello che il piano non prevede

**Dire:** "Due cose che succedono sempre. Una persona chiave in ferie proprio
nelle due settimane di etichettatura. E il fornitore che cambia versione del
modello mentre state misurando."

**Dire:** "Mettete due settimane di margine e decidete in anticipo chi
sostituisce chi. Nessun piano di tre mesi regge senza margine."

## Slide 85. Cosa mettere per iscritto prima di partire

**Dire:** "Tre righe, non un documento. Chi possiede la tassonomia e ogni
quanto la rivede. Chi guarda la coda, quando, e cosa fa se cresce. E le
risposte scritte alle sei domande di prima."

**Dire:** "Senza queste tre righe il pilota dipende dalla buona volontà di una
persona, e finisce quando quella persona cambia ufficio."

## Slide 86. Fermarsi è un esito legittimo

**Dire:** "Un binario che finisce. Il pilota serve a scoprire a basso costo se
conviene, non a dimostrare che conviene."

**Dire:** "Se dopo un mese i numeri non si muovono, si ferma, e avete imparato
qualcosa spendendo tre mesi invece di una piattaforma."

**Dire, guardando la telecamera:** "Ve lo dico adesso perché dopo, quando ci
avrete messo dentro tre mesi di lavoro, sarà più difficile dirlo."

---

# Blocco 6. Esercitazione (1:30 - 2:00)

Trenta minuti. Da remoto, senza stanze separate. Meno di quindici collegati,
quindi la chat si legge mentre si parla e si possono chiamare le persone per
nome.

## Slide 87. Sezione 6

**Dire:** "Ultima mezz'ora, e non faccio lezione. Tre tempi: dieci minuti da
soli, quindici insieme, cinque in chat."

**Fare:** incollare in chat il link alla griglia.

## Slide 88. Come funziona l'esercizio

**[clic]** "Dieci minuti da soli. Ognuno prende un processo che conosce e lo
scompone con la griglia. Microfoni chiusi."

**[clic]** "Poi quindici minuti insieme: ne scomponiamo uno dal vivo, e lo
scegliete voi."

**[clic]** "E cinque minuti finali in chat, tre domande, una riga a testa."

**Dire:** "Non vi metto in stanze separate. Da remoto, in una stanza da
quattro, di solito parla uno e gli altri tre aspettano che finisca. Preferisco
che ognuno provi con le proprie mani e poi lo facciamo insieme."

## Slide 89. Consegna

**Dire:** "La consegna è questa. Scegliete un processo della Fondazione. Poi lo
scomponete: un passo per riga."

**Dire, insistendo:** "Un passo per riga anche se sembra banale. Anzi,
soprattutto se sembra banale, perché è lì che si nascondono le integrazioni.
Scaricare un allegato è un passo. Aprire un foglio è un passo."

**Dire:** "E per ogni passo una parola sola nell'ultima colonna: integrazione,
AI, oppure umano."

## Slide 90. La griglia da compilare

**Fare:** ricordare il link in chat. Lasciare trenta secondi perché la aprano.

**Dire:** "Sei righe bastano. Se ve ne servono di più, quello che avete scelto
erano due processi, e conviene sceglierne uno."

**Dire:** "Chi preferisce può scriverla a mano su un foglio. L'importante è che
ognuno abbia la sua, perché serve fra dieci minuti."

## Slide 91. La griglia, compilata sull'helpdesk

**Dire:** "Questo è l'esempio, ed è il vostro helpdesk. Sette passi. Guardate
l'ultima colonna: tre AI, due umano, due integrazione o regola."

**Dire:** "Arrivate a una tabella così. Non più bella: così."

## Slide 92. Tre processi candidati

**Dire:** "Se non vi viene in mente niente, tre proposte. Rendicontazione di un
progetto, rassegna stampa e bandi, gestione delle iscrizioni."

**Dire:** "Ma un processo vostro è sempre meglio di uno dei miei."

**Fare:** chiedere. "Scrivete in chat quale avete scelto, anche solo due
parole. Mi serve dopo."

## Slide 93. Dieci minuti, ognuno per sé

**Fare:** lasciare questa slide condivisa per tutti e dieci i minuti. Tenere il
microfono aperto.

**Dire:** "Dieci minuti. Microfoni chiusi, telecamere come volete. Se avete una
domanda scrivetela in chat e vi rispondo mentre lavorate. Quando avete finito,
scrivete fatto."

**Fare, durante i dieci minuti:**
- leggere in chat i processi scelti
- decidere quale scomporre insieme: meglio uno che nessuno ha già risolto, e meglio uno proposto da chi non ha ancora parlato
- avvisare a tre minuti dalla fine: "tre minuti"

## Slide 94. Adesso ne scomponiamo uno insieme

Questo è il pezzo centrale della mezz'ora. Quindici minuti.

**Dire:** "Prendiamo quello di [nome], la rendicontazione. Lo facciamo insieme,
riga per riga, e lo compilo io mentre voi mi dettate."

**Fare:** condividere la griglia vuota, in un foglio o in un documento, e
compilarla davvero mentre parlano. Non usare la slide: usare un file
modificabile.

**Come condurre, una riga alla volta:**

1. **Dire:** "Primo passo. Cosa succede per primo, in ordine di tempo?"
   Aspettare. Scrivere quello che dicono, con le loro parole.
2. **Dire:** "Input: da dove arriva quello che serve a questo passo?"
3. **Dire:** "Decisione: in questo passo qualcuno decide qualcosa? Se sì, in
   base a quale regola?"
4. **Dire:** "Output: dove finisce il risultato?"
5. **E poi, la colonna che conta.** Non rispondere. **Dire:** "Ultima colonna.
   Questo passo è integrazione, AI o umano? Scrivetelo in chat."

**Fare:** aspettare le risposte in chat. Contarle ad alta voce.

**Se le risposte sono diverse, fermarsi.** **Dire:** "Ecco. Tre dicono AI, due
dicono umano. Non state sbagliando: la riga è ambigua. È esattamente quello
che vi ho detto mezz'ora fa, quando abbiamo visto che il modello sbaglia
l'urgenza undici volte su quaranta. Dove due persone non concordano, il
problema non è il modello: è che la regola non è ancora scritta."

**Dire, e questa è la frase da non perdere:** "E questo è il lavoro del passo
due del pilota. Non è un lavoro da consulente. È questo, che stiamo facendo
adesso, ripetuto per duecento richieste."

**Poi continuare con le righe successive**, più velocemente. Arrivare a sei
righe, non oltre.

**Chiudere dicendo:** "Contate le righe con AI. Su sei passi, quante ne
abbiamo? [dire il numero]. Il resto è idraulica e persone. È la stessa
proporzione dell'helpdesk."

**PIANO B, se in chat non arriva nessun processo:** prendere la gestione delle
iscrizioni ai corsi, che tutti conoscono, e condurla nello stesso modo,
chiedendo comunque a loro le righe. Non usare l'helpdesk: quello è già
scomposto nella slide precedente e non insegnerebbe niente.

## Slide 95. Le tre domande, in chat

**Dire:** "Cinque minuti, tre domande, una riga a testa in chat. Sul processo
che avete scomposto voi, non su quello che abbiamo fatto insieme."

**[clic]** "Qual è il passo che, automatizzato, fa risparmiare più tempo?"

**[clic]** "Qual è il passo dove un errore del sistema costa di più?"

**[clic]** "Quale numero misurereste dopo un mese per decidere se continuare?"

**Fare:** aspettare, poi leggere ad alta voce tre o quattro risposte, con il
nome di chi le ha scritte.

**Dire, quando emerge:** "Notate una cosa: molto spesso il passo che vale di
più e quello che rischia di più sono lo stesso passo. È il momento in cui la
lezione si chiude da sola: quello è il passo dove serve una persona, non
nonostante il valore, ma proprio per quello."

**Fare, a fine giornata:** salvare la chat. È un elenco di processi candidati
scritto dal personale della Fondazione, e vale più di queste slide.

## Slide 96. Guardate la chat

**Dire, dieci secondi, senza spiegare:** "Guardate la chat. Testo non
strutturato, in una chat, che nessuno rileggerà."

Pausa.

**Dire:** "Vi ricorda qualcosa?"

Avanti.

## Slide 97. Tre errori da evitare

**Dire:** "Chiusura. Sono le tre righe di apertura, girate al contrario."

**[clic]** "Automatizzare prima di misurare."

**[clic]** "Togliere l'umano troppo presto."

**[clic]** "Comprare la piattaforma prima di aver definito il processo."

## Slide 98. Che cosa vi portate a casa

**[clic]** "Un repository con dati, codice, griglia e queste slide, che gira
anche senza chiave API."

**[clic]** "Tre domande da fare a un fornitore, e una diagnosi per capire chi
ha sbagliato fra il modello e la tassonomia."

**[clic]** "E il compito per lunedì: una tassonomia da riscrivere sui vostri
corsi veri."

**Dire:** "Il terzo è il vero compito, ed è anche l'unico che non posso fare
io. Dieci minuti a settimana per un mese e il passo due è fatto."

## Slide 99. Materiali e contatti

**Dire:** "Tutto quello che avete visto è nel repository, link qui. Gira anche
senza chiave API, in modalità mock, così potete provare la forma dell'uscita
senza spendere niente."

**Dire:** "E la mia e-mail. Scrivetemi quando riscrivete la tassonomia: sono
curioso di vedere quante voci vi servono davvero."

**ATTENZIONE, da verificare prima della lezione:** oggi il repository è
privato, quindi quel link dà 404 a chi non è invitato. Tre strade: renderlo
pubblico, invitare i partecipanti, oppure togliere la riga e mandare il
materiale per e-mail. Il comando per renderlo pubblico è in HANDOFF.md.

## Slide 100. Grazie

**Dire:** "Grazie. Domande."

**Fare:** smettere di parlare. Aspettare. Da remoto il primo silenzio dura più
del previsto: non riempirlo.

**Se non arriva niente entro dieci secondi, dire:** "Ne faccio una io, che me
la fanno sempre: quanto costa? La risposta è che le chiamate al modello, su
trecento richieste al mese, sono la voce più piccola del conto. Il costo è la
persona che ogni trimestre guarda gli errori."

---

# Appendice. Le domande che arrivano sempre

Risposte pronte, in una frase ciascuna.

**"Quanto costa?"**
Le chiamate al modello su questi volumi sono la voce più piccola. Il costo
vero è il tempo di chi mantiene la tassonomia. Chiedete ai fornitori il costo
per mille richieste, non per token.

**"Ma i dati vanno negli Stati Uniti?"**
Dipende dal contratto e dalla configurazione, e non è una domanda a cui
risponde un informatico in una slide. È la domanda numero quattro delle sei
da mettere per iscritto.

**"Non è che poi ci sostituisce?"**
Su questo processo no, e non per gentilezza: perché tre passi su sette
richiedono di decidere qualcosa di cui qualcuno risponde. Quello che sostituisce
è lo smistamento, che è la parte che nessuno ama fare.

**"Possiamo farlo senza far uscire i dati?"**
Tecnicamente esistono modelli che girano dentro casa. Su trecento richieste al
mese il rapporto fra costo e beneficio è cattivo, e non è il primo problema da
risolvere. Se diventa un requisito, cambia il fornitore, non il disegno.

**"E se il modello sbaglia e mandiamo una risposta sbagliata?"**
Nel disegno che vi ho mostrato non può, perché il modello non invia. Se un
giorno lo farà inviare, quella è la domanda numero sei.

**"Quanto tempo ci vuole per partire?"**
Tre mesi fino alla decisione, di cui il primo è contare e il secondo
etichettare. Il pezzo tecnologico è il terzo ed è il più corto.

**"Chi lo fa da noi?"**
La segreteria per i primi due passi, chi sa già usare lo strumento per il
terzo, la direzione per la decisione. Se per il terzo non c'è nessuno, si
compra quel pezzo.

**"Perché non usiamo direttamente un agente che fa tutto?"**
Perché non sapreste dire dove ha sbagliato. Con sette passi separati, quando
qualcosa va storto sapete quale passo guardare.
