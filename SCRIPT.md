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
