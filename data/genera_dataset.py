"""Genera il dataset sintetico di richieste e le etichette di riferimento.

Le richieste sono inventate ma modellate sui canali reali della Fondazione:
cinque caselle e-mail, moduli di iscrizione sul sito, richieste da Moodle,
risposte aperte ai questionari Moodle e chat Zoom durante i corsi.

Uso:
    python data/genera_dataset.py
Scrive data/richieste.jsonl, data/etichette_oro.jsonl e i file in data/grezzi/.
"""
from __future__ import annotations

import json
from pathlib import Path

QUI = Path(__file__).parent

# Ogni voce: (id, canale, sorgente, mittente, testo, etichette oro)
# Etichette: corso, tipologia, urgenza, operatore
RICHIESTE = [
    # ---------- e-mail dirette ----------
    ("R001", "email", "iscrizioni@", "Comune di Cascina, Ufficio Personale",
     "Buongiorno, vorremmo iscrivere due dipendenti al corso sul nuovo Codice dei contratti "
     "del 18 settembre. Potete confermare la disponibilità dei posti e inviarci il modulo? Grazie.",
     dict(corso="contratti-pubblici", tipologia="iscrizione", urgenza="media", operatore="segreteria-didattica")),
    ("R002", "email", "segreteria@", "Dott.ssa R. (Provincia)",
     "Ho partecipato al corso Anticorruzione del 25 giugno ma non ho mai ricevuto l'attestato. "
     "Mi serve per il fascicolo formativo entro fine mese.",
     dict(corso="anticorruzione", tipologia="attestato", urgenza="media", operatore="segreteria-didattica")),
    ("R003", "email", "amministrazione@", "Ragioneria Comune di Empoli",
     "Con riferimento alla fattura n. 2026/311 relativa al corso Bilancio enti locali, segnaliamo che "
     "manca il CIG. Senza CIG non possiamo procedere al pagamento.",
     dict(corso="bilancio-enti-locali", tipologia="fatturazione", urgenza="media", operatore="amministrazione")),
    ("R004", "email", "formazione@", "Unione Comuni Valdera",
     "Salve, il corso Privacy e GDPR di domani mattina è confermato? Non abbiamo ricevuto il link Zoom.",
     dict(corso="privacy-gdpr", tipologia="accesso-piattaforma", urgenza="alta", operatore="tutor-piattaforma")),
    ("R005", "email", "info@", "Privato cittadino",
     "Organizzate corsi anche per liberi professionisti che lavorano con la PA? Sono interessato al tema PNRR.",
     dict(corso="digitalizzazione-pnrr", tipologia="informazioni", urgenza="bassa", operatore="segreteria-didattica")),
    ("R006", "email", "formazione@", "Segretario comunale",
     "Durante il corso IA nella PA il docente ha citato una circolare AgID sull'uso dei modelli generativi. "
     "Potreste inviarmi il riferimento preciso? Non lo trovo nelle slide.",
     dict(corso="ia-pa", tipologia="contenuti", urgenza="bassa", operatore="coordinamento-docenti")),
    ("R007", "email", "segreteria@", "Ufficio Tributi, Comune di Pontedera",
     "È la terza volta che scrivo per l'attestato del corso Bilancio. Nessuna risposta. "
     "Se non arriva entro venerdì dovrò segnalarlo al mio dirigente.",
     dict(corso="bilancio-enti-locali", tipologia="reclamo", urgenza="alta", operatore="direzione")),
    ("R008", "email", "iscrizioni@", "Comune di Lucca",
     "Il collega iscritto al corso Contratti del 18/9 è in malattia. Possiamo sostituirlo con un altro dipendente?",
     dict(corso="contratti-pubblici", tipologia="iscrizione", urgenza="media", operatore="segreteria-didattica")),
    ("R009", "email", "amministrazione@", "Azienda sanitaria",
     "Chiediamo se per il corso Digitalizzazione e PNRR sia possibile emettere fattura in split payment "
     "intestata alla nostra sede legale anziché al presidio.",
     dict(corso="digitalizzazione-pnrr", tipologia="fatturazione", urgenza="bassa", operatore="amministrazione")),
    ("R010", "email", "info@", "Ordine professionale",
     "Complimenti per il corso di ieri sull'anticorruzione: chiaro e concreto. Lo segnaleremo ai nostri iscritti.",
     dict(corso="anticorruzione", tipologia="feedback", urgenza="bassa", operatore="direzione")),
    ("R011", "email", "formazione@", "Dipendente comunale",
     "Non riesco a entrare su Moodle, mi dice password errata anche dopo il reset. Il corso inizia tra un'ora.",
     dict(corso="nessuno", tipologia="accesso-piattaforma", urgenza="alta", operatore="tutor-piattaforma")),
    ("R012", "email", "segreteria@", "Responsabile formazione ente",
     "Avete un calendario dei corsi dell'ultimo trimestre 2026 da condividere con i nostri uffici?",
     dict(corso="nessuno", tipologia="informazioni", urgenza="bassa", operatore="segreteria-didattica")),
    # ---------- moduli dal sito ----------
    ("R013", "form_sito", "pagina iscrizione: Codice contratti pubblici", "Comune di Capannori",
     "Nome: M. Bianchi. Ente: Comune di Capannori. Note: partecipo solo alla seconda giornata, "
     "è previsto uno sconto?",
     dict(corso="contratti-pubblici", tipologia="iscrizione", urgenza="media", operatore="segreteria-didattica")),
    ("R014", "form_sito", "pagina iscrizione: IA nella PA", "Comune di Viareggio",
     "Note: siamo in 6, chiediamo tariffa per gruppo e se il corso dà crediti formativi riconosciuti.",
     dict(corso="ia-pa", tipologia="informazioni", urgenza="media", operatore="segreteria-didattica")),
    ("R015", "form_sito", "modulo contatti", "Sconosciuto",
     "Vorrei ricevere la newsletter dei corsi.",
     dict(corso="nessuno", tipologia="altro", urgenza="bassa", operatore="da-assegnare")),
    ("R016", "form_sito", "pagina iscrizione: Privacy e GDPR", "Comune di Massarosa",
     "Note: iscrizione inviata due volte per errore, annullare il doppione.",
     dict(corso="privacy-gdpr", tipologia="iscrizione", urgenza="media", operatore="segreteria-didattica")),
    # ---------- richieste via Moodle ----------
    ("R017", "moodle_messaggio", "corso: Bilancio enti locali", "Partecipante",
     "Le slide della lezione 3 non si aprono, il file risulta corrotto.",
     dict(corso="bilancio-enti-locali", tipologia="accesso-piattaforma", urgenza="media", operatore="tutor-piattaforma")),
    ("R018", "moodle_messaggio", "corso: Anticorruzione", "Partecipante",
     "Il questionario finale mi dà 'tentativi esauriti' ma non l'ho mai completato. Senza questionario niente attestato?",
     dict(corso="anticorruzione", tipologia="attestato", urgenza="media", operatore="tutor-piattaforma")),
    ("R019", "moodle_messaggio", "corso: IA nella PA", "Partecipante",
     "Nella lezione sui prompt il docente ha detto che pubblicherà un esempio di regolamento interno. Dove lo trovo?",
     dict(corso="ia-pa", tipologia="contenuti", urgenza="bassa", operatore="coordinamento-docenti")),
]

# Chat Zoom grezza: testo non strutturato. Solo alcune righe sono richieste.
ZOOM_CHAT = """[10:02] Segreteria Promo PA: Buongiorno a tutti, benvenuti al corso Codice dei contratti pubblici.
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
"""

# Risposte aperte del questionario di gradimento Moodle (corso Privacy e GDPR).
# Alcune contengono richieste che oggi vanno perse.
MOODLE_QUESTIONARIO = [
    ("Q01", "Corso ben strutturato, docente preparata."),
    ("Q02", "Troppo veloce la parte sulle valutazioni d'impatto. Servirebbe un modulo dedicato."),
    ("Q03", "Non ho ricevuto il materiale integrativo promesso a lezione (il modello di registro trattamenti)."),
    ("Q04", "Tutto ok."),
    ("Q05", "Ci sarebbe interesse nel nostro ente per un'edizione in presenza a Lucca, siamo circa 15 persone."),
    ("Q06", "L'audio della seconda giornata era pessimo, ho perso metà lezione. Chiedo se esiste la registrazione."),
    ("Q07", "Grazie, molto utile per il mio lavoro quotidiano."),
    ("Q08", "Avrei bisogno dell'attestato con il numero di ore indicato, per il nostro piano formativo."),
]

# Etichette oro per le richieste estratte dai grezzi (l'estrattore deve trovarle).
ESTRATTE_ORO = [
    ("Z-1041", "zoom_chat", "corso: Codice contratti, 2026-09-03", "Comune di Pisa - L.R.",
     "le slide verranno inviate dopo?",
     dict(corso="contratti-pubblici", tipologia="contenuti", urgenza="bassa", operatore="coordinamento-docenti")),
    ("Z-1048", "zoom_chat", "corso: Codice contratti, 2026-09-03", "Comune di Livorno - A.F.",
     "la soglia per l'affidamento diretto vale anche per i servizi di ingegneria?",
     dict(corso="contratti-pubblici", tipologia="contenuti", urgenza="bassa", operatore="coordinamento-docenti")),
    ("Z-1141", "zoom_chat", "corso: Codice contratti, 2026-09-03", "Comune di Lucca - P.D.",
     "l'attestato viene rilasciato automaticamente o dobbiamo richiederlo?",
     dict(corso="contratti-pubblici", tipologia="attestato", urgenza="bassa", operatore="segreteria-didattica")),
    ("Z-1220", "zoom_chat", "corso: Codice contratti, 2026-09-03", "Provincia - G.M.",
     "sarebbe utile un corso di approfondimento solo sulla parte esecuzione del contratto",
     dict(corso="contratti-pubblici", tipologia="feedback", urgenza="bassa", operatore="direzione")),
    ("Q02", "moodle_questionario", "corso: Privacy e GDPR", "Anonimo",
     "Troppo veloce la parte sulle valutazioni d'impatto. Servirebbe un modulo dedicato.",
     dict(corso="privacy-gdpr", tipologia="feedback", urgenza="bassa", operatore="direzione")),
    ("Q03", "moodle_questionario", "corso: Privacy e GDPR", "Anonimo",
     "Non ho ricevuto il materiale integrativo promesso a lezione (il modello di registro trattamenti).",
     dict(corso="privacy-gdpr", tipologia="contenuti", urgenza="media", operatore="coordinamento-docenti")),
    ("Q05", "moodle_questionario", "corso: Privacy e GDPR", "Anonimo",
     "Ci sarebbe interesse nel nostro ente per un'edizione in presenza a Lucca, siamo circa 15 persone.",
     dict(corso="privacy-gdpr", tipologia="informazioni", urgenza="bassa", operatore="segreteria-didattica")),
    ("Q06", "moodle_questionario", "corso: Privacy e GDPR", "Anonimo",
     "L'audio della seconda giornata era pessimo, ho perso metà lezione. Chiedo se esiste la registrazione.",
     dict(corso="privacy-gdpr", tipologia="reclamo", urgenza="media", operatore="direzione")),
    ("Q08", "moodle_questionario", "corso: Privacy e GDPR", "Anonimo",
     "Avrei bisogno dell'attestato con il numero di ore indicato, per il nostro piano formativo.",
     dict(corso="privacy-gdpr", tipologia="attestato", urgenza="media", operatore="segreteria-didattica")),
]


def main() -> None:
    grezzi = QUI / "grezzi"
    grezzi.mkdir(exist_ok=True)
    (grezzi / "zoom_chat_contratti_2026-09-03.txt").write_text(ZOOM_CHAT, encoding="utf-8")
    with (grezzi / "moodle_questionario_privacy.csv").open("w", encoding="utf-8") as f:
        f.write("id;risposta_aperta\n")
        for qid, testo in MOODLE_QUESTIONARIO:
            f.write(f"{qid};{testo}\n")

    with (QUI / "richieste.jsonl").open("w", encoding="utf-8") as f:
        for rid, canale, sorgente, mittente, testo, _ in RICHIESTE:
            f.write(json.dumps(dict(id=rid, canale=canale, sorgente=sorgente,
                                    mittente=mittente, testo=testo), ensure_ascii=False) + "\n")

    with (QUI / "etichette_oro.jsonl").open("w", encoding="utf-8") as f:
        for rid, canale, sorgente, mittente, testo, oro in RICHIESTE + ESTRATTE_ORO:
            f.write(json.dumps(dict(id=rid, canale=canale, testo=testo, **oro),
                               ensure_ascii=False) + "\n")
    print("Scritti richieste.jsonl, etichette_oro.jsonl e data/grezzi/")


if __name__ == "__main__":
    main()
