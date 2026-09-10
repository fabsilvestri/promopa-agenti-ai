"""Costruisce la lezione a partire da Template_RSTLess.pptx.

Regola dura: massimo 3 bullet per slide. Se servono di più, la slide si
sdoppia con titolo "Titolo 1/n".
"""
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
import copy

TPL = "slides/tools/Template_RSTLess.pptx"
OUT = "slides/Lezione_15_settembre_Agenti_AI_PromoPA.pptx"
FIG = "slides/tools/fig/"
BORD = RGBColor(0x82, 0x24, 0x33); NERO = RGBColor(0x21, 0x21, 0x21); GRIG = RGBColor(0x59, 0x59, 0x59)
AZZ = RGBColor(0xE9, 0xF1, 0xF8); VERDE = RGBColor(0x2C, 0x6E, 0x49)
FOOTER = "Promo PA Fondazione  |  Agenti AI per i processi interni  |  15.09.2026"

prs = Presentation(TPL)
W, H = prs.slide_width, prs.slide_height  # 9144000 x 5143500

# --- footer nel master
for shp in prs.slide_master.shapes:
    if shp.has_text_frame and "Project name" in shp.text_frame.text:
        r = shp.text_frame.paragraphs[0].runs[0]
        r.text = FOOTER

# --- elimina le slide di esempio
sldIdLst = prs.slides._sldIdLst
for sldId in list(sldIdLst):
    prs.part.drop_rel(sldId.rId)
    sldIdLst.remove(sldId)

L_TITLE, L_SECTION, L_BODY, L_TWO, L_TITLEONLY, L_BLANK = [prs.slide_layouts[i] for i in range(6)]

BULLET_COUNT_MAX = 3


def _style_title(ph, size=26):
    tf = ph.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    for r in p.runs:
        r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = BORD; r.font.name = "Arial"


def _bullets(tf, items, size=17, color=NERO, space=10):
    """Scrive bullet veri (buChar), uno per paragrafo. Sottoelenchi con tuple (testo, [sub])."""
    assert len(items) <= BULLET_COUNT_MAX, f"troppi bullet: {items}"
    tf.word_wrap = True
    first = True
    for it in items:
        sub = None
        if isinstance(it, tuple):
            it, sub = it
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        _set_bullet(p, it, size, color, space, level=0)
        if sub:
            for s in sub:
                p2 = tf.add_paragraph()
                _set_bullet(p2, s, size - 3, GRIG, space - 4, level=1)


def _set_bullet(p, text, size, color, space, level=0):
    p.text = ""
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.color.rgb = color; r.font.name = "Arial"
    p.space_after = Pt(space)
    pPr = p._p.get_or_add_pPr()
    marL = 285750 if level == 0 else 571500
    pPr.set("marL", str(marL)); pPr.set("indent", str(-228600)); pPr.set("lvl", str(level))
    for tag in ("a:buNone", "a:buChar", "a:buClr", "a:buFont"):
        for e in pPr.findall(qn(tag)):
            pPr.remove(e)
    buClr = etree.SubElement(pPr, qn("a:buClr")); c = etree.SubElement(buClr, qn("a:srgbClr")); c.set("val", "822433")
    buFont = etree.SubElement(pPr, qn("a:buFont")); buFont.set("typeface", "Arial")
    bu = etree.SubElement(pPr, qn("a:buChar")); bu.set("char", "•" if level == 0 else "–")


def _textbox(slide, x, y, w, h, text, size=14, color=NERO, bold=False, align=PP_ALIGN.LEFT, font="Arial", fill=None, anchor=MSO_ANCHOR.TOP, italic=False):
    tb = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(h))
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Emu(90000); tf.margin_top = tf.margin_bottom = Emu(60000)
    if fill is not None:
        tb.fill.solid(); tb.fill.fore_color.rgb = fill
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run(); r.text = line
        r.font.size = Pt(size); r.font.color.rgb = color; r.font.bold = bold; r.font.name = font; r.font.italic = italic
    return tb


def _code(slide, x, y, w, h, code, size=11):
    tb = _textbox(slide, x, y, w, h, code, size=size, color=NERO, font="Courier New", fill=AZZ)
    tb.line.color.rgb = RGBColor(0xC9, 0xD6, 0xE3)
    return tb


def _notes(slide, text):
    if text:
        slide.notes_slide.notes_text_frame.text = text


def title_slide(title, subtitle, notes=""):
    s = prs.slides.add_slide(L_TITLE)
    s.shapes.title.text = title
    for r in s.shapes.title.text_frame.paragraphs[0].runs:
        r.font.size = Pt(34); r.font.bold = True; r.font.color.rgb = BORD; r.font.name = "Arial"
    for ph in s.placeholders:
        if ph.placeholder_format.idx == 1:
            ph.text = subtitle
            for p in ph.text_frame.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(16); r.font.color.rgb = GRIG; r.font.name = "Arial"
    # rimuove i placeholder inutilizzati (foto e testi dei relatori)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx in (2, 3, 4, 5):
            ph._element.getparent().remove(ph._element)
    _textbox(s, 2700000, 3835000, 6200000, 420000, "Fabrizio Silvestri  |  Sapienza Università di Roma, DIAG", size=14, color=GRIG, anchor=MSO_ANCHOR.MIDDLE)
    _notes(s, notes)
    return s


def section(title, subtitle="", notes=""):
    s = prs.slides.add_slide(L_SECTION)
    s.shapes.title.text = title
    for r in s.shapes.title.text_frame.paragraphs[0].runs:
        r.font.size = Pt(32); r.font.bold = True; r.font.color.rgb = BORD; r.font.name = "Arial"
    for ph in s.placeholders:
        if ph.placeholder_format.idx == 1:
            ph.text = subtitle
            for p in ph.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                pPr = p._p.get_or_add_pPr()
                for e in list(pPr):
                    if e.tag in (qn("a:buChar"), qn("a:buFont"), qn("a:buClr"), qn("a:buNone")):
                        pPr.remove(e)
                etree.SubElement(pPr, qn("a:buNone"))
                pPr.set("marL", "0"); pPr.set("indent", "0")
                for r in p.runs:
                    r.font.size = Pt(16); r.font.color.rgb = GRIG; r.font.name = "Arial"
    _notes(s, notes)
    return s


def bullets(title, items, notes="", size=20):
    s = prs.slides.add_slide(L_BODY)
    s.shapes.title.text = title; _style_title(s.shapes.title)
    body = [ph for ph in s.placeholders if ph.placeholder_format.idx == 1][0]
    body.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    body.top = Emu(1250000)
    _bullets(body.text_frame, items, size=size, space=14)
    _notes(s, notes)
    return s


def bullets_image(title, items, image, notes="", img_w_frac=0.52, size=17):
    """Testo a sinistra, immagine a destra."""
    s = prs.slides.add_slide(L_TITLEONLY)
    s.shapes.title.text = title; _style_title(s.shapes.title)
    left_w = int(8784000 * (1 - img_w_frac)) - 90000
    tb = s.shapes.add_textbox(Emu(180000), Emu(1134300), Emu(left_w), Emu(3400000))
    tb.text_frame.margin_left = Emu(0)
    _bullets(tb.text_frame, items, size=size)
    ix = 180000 + left_w + 180000
    iw = 8964000 - ix
    pic = s.shapes.add_picture(image, Emu(ix), Emu(1180000), width=Emu(iw))
    if pic.height > 3400000:
        ratio = 3400000 / pic.height
        pic.height = Emu(3400000); pic.width = Emu(int(pic.width * ratio))
        pic.left = Emu(ix + (iw - pic.width) // 2)
    _notes(s, notes)
    return s


def image_full(title, image, caption="", notes="", max_h=3000000):
    s = prs.slides.add_slide(L_TITLEONLY)
    s.shapes.title.text = title; _style_title(s.shapes.title)
    pic = s.shapes.add_picture(image, Emu(180000), Emu(1150000), width=Emu(8784000))
    if pic.height > max_h:
        ratio = max_h / pic.height
        pic.height = Emu(max_h); pic.width = Emu(int(pic.width * ratio))
        pic.left = Emu((W - pic.width) // 2)
    if caption:
        _textbox(s, 180000, 4230000, 8784000, 300000, caption, size=11, color=GRIG, italic=True)
    _notes(s, notes)
    return s


def image_top_bullets(title, image, items, notes="", img_h=1500000, size=17):
    """Figura larga in alto, bullet sotto."""
    s = prs.slides.add_slide(L_TITLEONLY)
    s.shapes.title.text = title; _style_title(s.shapes.title)
    pic = s.shapes.add_picture(image, Emu(180000), Emu(1120000), height=Emu(img_h))
    if pic.width > 8784000:
        ratio = 8784000 / pic.width
        pic.width = Emu(8784000); pic.height = Emu(int(pic.height * ratio))
    pic.left = Emu((W - pic.width) // 2)
    y = 1120000 + pic.height + 150000
    tb = s.shapes.add_textbox(Emu(180000), Emu(y), Emu(8784000), Emu(4600000 - y))
    tb.text_frame.margin_left = Emu(0)
    _bullets(tb.text_frame, items, size=size, space=8)
    _notes(s, notes)
    return s


def bullets_code(title, items, code, notes="", code_frac=0.55, size=16, code_size=10.5):
    s = prs.slides.add_slide(L_TITLEONLY)
    s.shapes.title.text = title; _style_title(s.shapes.title)
    left_w = int(8784000 * (1 - code_frac)) - 90000
    tb = s.shapes.add_textbox(Emu(180000), Emu(1134300), Emu(left_w), Emu(3400000))
    tb.text_frame.margin_left = Emu(0)
    _bullets(tb.text_frame, items, size=size)
    cx = 180000 + left_w + 180000
    _code(s, cx, 1150000, 8964000 - cx, 3200000, code, size=code_size)
    _notes(s, notes)
    return s


def code_full(title, code, notes="", size=11):
    s = prs.slides.add_slide(L_TITLEONLY)
    s.shapes.title.text = title; _style_title(s.shapes.title)
    _code(s, 180000, 1150000, 8784000, 3200000, code, size=size)
    _notes(s, notes)
    return s


def numbers(title, stats, items, notes=""):
    """Tre numeri grandi in alto, tre bullet sotto."""
    s = prs.slides.add_slide(L_TITLEONLY)
    s.shapes.title.text = title; _style_title(s.shapes.title)
    n = len(stats); gap = 180000; cw = (8784000 - gap * (n - 1)) // n
    for i, (num, lab) in enumerate(stats):
        x = 180000 + i * (cw + gap)
        box = s.shapes.add_shape(1, Emu(x), Emu(1150000), Emu(cw), Emu(1350000))
        box.fill.solid(); box.fill.fore_color.rgb = AZZ; box.line.fill.background()
        box.shadow.inherit = False
        _textbox(s, x, 1180000, cw, 750000, num, size=40, color=BORD, bold=True, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        _textbox(s, x, 1930000, cw, 520000, lab, size=13, color=GRIG, align=PP_ALIGN.CENTER)
    tb = s.shapes.add_textbox(Emu(180000), Emu(2700000), Emu(8784000), Emu(1900000))
    tb.text_frame.margin_left = Emu(0)
    _bullets(tb.text_frame, items, size=16)
    _notes(s, notes)
    return s


# =====================================================================
# CONTENUTO
# =====================================================================

title_slide("Agenti AI per i processi interni",
            "Dal caso helpdesk formazione a un pilota misurabile\nPromo PA Fondazione, 15 settembre 2026",
            notes="Seconda lezione dopo quella del 22 giugno su ChatGPT. Oggi si passa dallo strumento personale al processo. Materiale e codice: github (vedi ultima slide).")

# ---------- 1. Riaggancio ----------
section("1. Riaggancio e tesi della giornata", "10 minuti", notes="Chiedere: chi ha usato Progetti o GPT personalizzati da giugno? Due minuti di giro di tavolo.")

bullets("Da giugno a oggi", [
    "A giugno: ChatGPT come collega. Prompt, Progetti, documenti, RAG",
    "Oggi: dal collega al processo. Cosa succede quando l'AI entra in un flusso di lavoro",
    "La vostra e-mail del 2 settembre è il caso di studio: helpdesk formazione",
], notes="Richiamare che ChatGPT Business è già in uso in Fondazione: tutto ciò che vedremo si può provare lì.")

image_top_bullets("Chatbot, workflow, agente", FIG + "chatbot_workflow_agente.png", [
    "Un chatbot risponde. Non agisce",
    "Un workflow segue passi decisi da noi; l'AI sta dentro alcuni passi",
    "Un agente decide da solo i passi. Serve raramente, costa controllo",
], img_h=1650000,
    notes="Tesi provocatoria ma vera: la maggior parte dei 'processi ripetitivi' vuole un workflow con AI dentro, non un agente autonomo. L'autonomia si compra con la prevedibilità.")

bullets("La tesi in tre righe", [
    "Prima si scompone il processo, poi si decide cosa automatizzare",
    "Dove serve giudizio o responsabilità, resta un punto di controllo umano",
    "Si misura prima di automatizzare, e si rimisura dopo",
], notes="Queste tre righe tornano alla fine come 'tre errori da evitare'.")

# ---------- 2. Anatomia ----------
section("2. Anatomia di un sistema agentico", "20 minuti", notes="Vocabolario minimo per parlare con fornitori e consulenti senza farsi vendere un agente quando serve una regola.")

bullets_image("I cinque pezzi 1/2", [
    "Modello: legge testo, produce testo o dati strutturati. Non sa nulla di voi",
    "Strumenti: e-mail, Zoom, Moodle, sito. Il modello li usa, non li possiede",
    "Memoria: tassonomia, storico, regole scritte da voi",
], FIG + "anatomia_agente.png", img_w_frac=0.50,
    notes="Il modello è la parte più famosa e la meno importante dal punto di vista del processo: cambia ogni sei mesi. Tassonomia e strumenti restano.")

bullets_image("I cinque pezzi 2/2", [
    "Ciclo di azione: leggi, decidi, agisci, verifica. Poi ricomincia",
    "Punto di controllo umano: soglia di confidenza, coda da verificare, invio manuale",
    "Un sistema senza punto di controllo non è coraggioso, è incompleto",
], FIG + "anatomia_agente.png", img_w_frac=0.50,
    notes="Il punto di controllo è progettato, non aggiunto dopo. Se il fornitore non sa dirvi dove sta, la risposta è 'da nessuna parte'.")

bullets_image("Pattern utili 1/2", [
    "Routing: una richiesta entra, un destinatario esce. Sotto soglia, coda umana",
    "Estrazione strutturata: da testo libero a campi fissi (chi, cosa, quando)",
    "Sono i due pattern che coprono il vostro caso quasi per intero",
], FIG + "pattern.png", img_w_frac=0.58,
    notes="Anthropic e OpenAI usano nomi diversi per gli stessi pattern; l'idea è la stessa: dare al modello un compito piccolo e un formato di uscita rigido.")

bullets("Pattern utili 2/2", [
    "Orchestratore e worker: un modello spezza il compito, altri lo eseguono. Utile per rendicontazioni lunghe",
    "Valutatore: un secondo passaggio controlla il primo. Utile prima dell'invio",
    "Regola d'oro: compito piccolo, formato di uscita rigido, un umano dove costa sbagliare",
], notes="Non entrare nei dettagli di orchestrazione: basta che riconoscano i nomi quando li leggono in un'offerta.")

bullets("Quando NON usare un agente", [
    "Se la regola si scrive in un 'se... allora', è una regola. Non serve un modello",
    "Se l'errore costa più del tempo risparmiato, serve un umano, non un agente",
    "Se non avete dati per misurarlo, non sapete se funziona. Prima i dati",
], notes="Esempio: 'assegna all'amministrazione tutto ciò che è fatturazione' è una regola. 'Capisci se questa e-mail parla di fatturazione' è AI.")

# ---------- 3. Il caso ----------
section("3. Il caso helpdesk formazione", "30 minuti, con demo", notes="Dati forniti da Matteo Baesso l'8 settembre: 300 richieste/mese, 5 caselle, nessuno strumento di tracciamento.")

numbers("I vostri numeri", [("~300", "richieste al mese"), ("5", "caselle e-mail diverse"), ("0", "strumenti di tracciamento")], [
    "Canali: e-mail dirette, pagine di iscrizione sul sito, Moodle",
    "Persi quasi del tutto: risposte aperte dei questionari Moodle e chat Zoom",
    "Chi risponde: chi ha la responsabilità sul tema. Funziona finché tutti ricordano tutto",
], notes="300 al mese sono 15 al giorno lavorativo. Non è volume da sistema complesso: è volume da 'una tabella e una regola di smistamento'.")

bullets_image("Le quattro esigenze", [
    "Solo due delle quattro hanno bisogno di un modello",
    "Le altre due sono integrazione e workflow: si risolvono senza AI, e vanno risolte prima",
    "Ordine consigliato: prima 1, 3 e 4, poi la 2",
], FIG + "mappa_esigenze.png", img_w_frac=0.62,
    notes="L'ordine è controintuitivo: la 2 (Zoom e Moodle) è la più affascinante e la meno urgente. Senza il contenitore unico, le richieste estratte non hanno dove andare.")

bullets("Esigenza 1: repository unico", [
    "Non è AI. È un contenitore più dei connettori dalle 5 caselle e dai moduli del sito",
    "Va bene anche un foglio condiviso o un ticketing gratuito, purché sia uno solo",
    "Da qui in poi ogni richiesta ha un id, uno stato, un responsabile",
], notes="Menzionare strumenti a basso codice: Make, Zapier, n8n, o le automazioni di Microsoft 365 / Google Workspace che già pagano.")

bullets_code("Esigenza 2: Zoom e Moodle", [
    "Testo non strutturato: 17 righe di chat, 4 richieste vere",
    "Il modello separa segnale e rumore e riporta le parole dell'utente",
    "Non riassume, non corregge, non inventa: solo estrae",
], """[10:03] Comune di Pisa: buongiorno
[10:11] Comune di Pisa: le slide verranno
        inviate dopo?
[10:25] Unione Valdera: non sento bene...
[10:26] Unione Valdera: ok risolto
[10:48] Comune di Livorno: domanda per il
        docente: la soglia per l'affidamento
        diretto vale anche per i servizi
        di ingegneria?
[11:41] Comune di Lucca: l'attestato viene
        rilasciato automaticamente?
[12:20] Provincia: sarebbe utile un corso
        sulla parte esecuzione del contratto
[12:29] Comune di Pisa: grazie, ottimo corso""", code_frac=0.52,
    notes="Righe evidenziate a voce: 10:11, 10:48, 11:41, 12:20 sono richieste. 10:25 no: l'utente dice 'risolto'. 12:29 è un ringraziamento, non un feedback azionabile.")

bullets_code("Esigenza 3: classificazione 1/2", [
    "La tassonomia la scrivete voi, in un file. Il modello la applica",
    "Gli operatori sono ruoli, non persone: così non invecchia",
    "Cambiare un corso non richiede di toccare il prompt",
], """# data/tassonomia.yaml
tipologie:
  - id: attestato
    descrizione: "Rilascio, correzione
      o reinvio dell'attestato"
  - id: fatturazione
    descrizione: "Fatture, CIG, split
      payment, pagamenti"
operatori:
  - id: segreteria-didattica
    competenze: [iscrizione, attestato,
                 informazioni]
  - id: amministrazione
    competenze: [fatturazione]
soglia_confidenza: 0.7""", code_frac=0.50,
    notes="Il file è nel repository. In demo cambieremo una voce e rifaremo la classificazione senza toccare il prompt.")

bullets_code("Esigenza 3: classificazione 2/2", [
    "Output strutturato: il modello restituisce questo oggetto o un errore. Mai testo libero",
    "La confidenza è dichiarata e decide se assegnare o fermarsi",
    "Sotto 0,7 la richiesta va in coda umana. È il punto di controllo",
], """{
  "corso": "bilancio-enti-locali",
  "tipologia": "reclamo",
  "urgenza": "alta",
  "operatore": "direzione",
  "confidenza": 0.89,
  "campo_meno_sicuro": "urgenza",
  "riassunto": "Pontedera: terzo sollecito
    per l'attestato, minaccia escalation
    entro venerdì"
}""", code_frac=0.48,
    notes="Esempio R007. Il reclamo prevale sull'oggetto (attestato): regola scritta nel prompt di sistema, non dedotta dal modello.")

bullets("Esigenza 4: tracciamento e follow-up", [
    "Stati e scadenze sono deterministici: nuova, presa in carico, in attesa, chiusa. Nessuna AI",
    "L'AI scrive la bozza di risposta; l'operatore la rivede e la invia",
    "Segnaposto obbligatori dove il sistema non sa: [data], [importo], [link]",
], notes="La bozza con segnaposto è una scelta di progetto: preferiamo un buco visibile a una data inventata.")

image_full("L'architettura, tutta insieme", FIG + "pipeline.png",
           caption="Arancio: passi con un modello. Verde: integrazione o umano. Un workflow, non un agente autonomo.",
           notes="Contare i passi con AI: tre su sette. Il resto è idraulica. È il messaggio centrale della lezione.")

bullets("Demo dal vivo: cosa vedrete", [
    "Un GPT personalizzato in ChatGPT Business con la tassonomia come file di conoscenza",
    "La stessa logica in 200 righe di Python con output strutturato e valutazione",
    "La chat Zoom grezza che diventa 4 righe in tabella",
], notes="Sequenza in demo/README.md. Piano B senza rete: demo/output_esempio. Tempo: 10 min GPT, 10 min codice, 10 min discussione.")

image_full("Demo: il risultato", FIG + "tabella_demo.png",
           caption="Righe rosa: confidenza sotto soglia, nessuna assegnazione automatica. Righe gialle: urgenza alta.",
           notes="Fermarsi su Q06: 'l'audio era pessimo, esiste la registrazione?' È reclamo o feedback? Il modello non è sicuro (0,66) e lo dice. Decide un umano. Comportamento voluto.")

code_full("Demo: una bozza di risposta (R007)", """Gentile Ufficio Tributi,

ha ragione: tre solleciti senza risposta non sono accettabili e ce ne
scusiamo. Abbiamo verificato la sua partecipazione al corso Bilancio e
contabilità degli enti locali e l'attestato le sarà inviato a questo
indirizzo entro [data, prima di venerdì].

Se non dovesse riceverlo, può scrivere direttamente a [contatto responsabile].

Cordiali saluti,
Segreteria Promo PA""", size=13,
    notes="Due segnaposto: la data e il contatto. Il modello non li conosce e non li inventa. L'operatore li riempie in dieci secondi.")

# ---------- 4. Limiti ----------
section("4. Limiti e rischi", "15 minuti", notes="Senza giri di parole. Questa parte serve a evitare che qualcuno compri qualcosa a ottobre.")

bullets("L'accuratezza si misura, non si stima", [
    "Serve un campione etichettato a mano: 100-200 richieste, due persone, poi confronto",
    "Dove le due persone non concordano, il problema è la tassonomia, non il modello",
    "Esempio dal repository: regole a parole chiave arrivano al 50% tutto corretto. Il modello si misura in aula",
], notes="In src/helpdesk_agent/valuta.py. Il backend 'mock' (regole) serve proprio a mostrare quanto sia facile sentirsi soddisfatti senza numeri.")

bullets("Dati personali", [
    "Le richieste contengono nomi, enti e a volte situazioni personali (malattia, contenziosi)",
    "Al modello serve il testo della richiesta, non lo storico del mittente: minimizzazione",
    "Due documenti prima del pilota: registro dei trattamenti e DPA con il fornitore",
], notes="Verificare con il DPO: base giuridica, sede di trattamento dei dati OpenAI, necessità di DPIA se si aggiungono risposte automatiche.")

bullets("Quadro normativo 1/2", [
    "AI Act, art. 4: alfabetizzazione del personale, obbligatoria dal febbraio 2025. Questa lezione ne fa parte",
    "AI Act, art. 50: trasparenza, in vigore dal 2 agosto 2026, non rinviata. Se un'AI parla con le persone, va detto",
    "Alto rischio (Allegato III): rinviato al dicembre 2027 dall'Omnibus. Lo smistamento amministrativo non rientra",
], notes="Fonti: Reg. UE 2024/1689; Reg. UE 2026/1744 (AI Omnibus, pubblicato il 24 luglio 2026, in vigore dal 27). L'omnibus ha riscritto l'art. 4: la data resta il 2 febbraio 2025, ma l'obbligo passa da garantire un livello di competenza ad adottare misure proporzionate. Dettagli e fonti in docs/normativa.md. Finché l'invio resta umano, art. 50 non scatta per la risposta.")

bullets("Quadro normativo 2/2", [
    "Legge 132/2025, art. 14: l'AI è di supporto, la responsabilità del provvedimento resta alla persona",
    "Linee guida AgID per l'IA nella PA: analisi, rischi, progettazione, monitoraggio. Il pilota le ricalca",
    "GDPR: base giuridica e responsabile del trattamento vanno scritti prima, non dopo",
], notes="Non fare l'avvocato. Art. 14 vincola le PA, non la Fondazione: lo citiamo perché è il metro con cui gli enti clienti guarderanno il servizio. Linee guida AgID approvate in Conferenza Unificata il 10 settembre 2025. Il messaggio è: il caso è nel perimetro semplice, a condizione che invio e decisioni restino umani e che i due documenti esistano.")

bullets("Manutenzione", [
    "La tassonomia invecchia: nuovi corsi, nuovi ruoli. Qualcuno la possiede e l'aggiorna",
    "Il modello cambia: ogni cambio di versione si rimisura sul campione etichettato",
    "La coda umana è il termometro: se supera il 30%, si rivede la tassonomia, non il modello",
], notes="Il costo vero non è la licenza: è la persona che ogni trimestre guarda gli errori e aggiorna il file.")

# ---------- 5. Pilota ----------
section("5. Dal caso d'uso al pilota", "15 minuti", notes="docs/pilota_4_passi.md ha le stesse informazioni con qualche dettaglio in più.")

image_top_bullets("Quattro passi 1/2", FIG + "quattro_passi.png", [
    "Audit: contare le richieste per canale, cronometrare la prima risposta, compilare la griglia",
    "Tassonomia e dati: scrivere il file, etichettare 100-200 richieste storiche a mano",
    "Senza questi due passi il terzo è un giocattolo",
], img_h=1350000,
    notes="Tempi indicativi: 1-2 settimane il primo, 2 il secondo. Il lavoro è della segreteria, non di un consulente.")

image_top_bullets("Quattro passi 2/2", FIG + "quattro_passi.png", [
    "Prototipo a basso codice: contenitore unico, connettori, classificatore, coda da verificare",
    "Un mese di metriche, poi decidere: estendere, correggere o fermare",
    "L'invio resta umano per tutto il pilota",
], img_h=1350000,
    notes="Fermarsi è un esito legittimo. Il pilota serve a scoprirlo a basso costo.")

bullets("Metriche decise prima di partire", [
    "Accuratezza per campo sul campione: sotto l'80% su tipologia e operatore il sistema fa perdere tempo",
    "Tempo alla prima risposta e ore di segreteria a settimana: prima e dopo",
    "Quota di richieste in coda umana: è la misura di quanto vi fidate, e di quanto potete fidarvi",
], notes="Le soglie sono punti di partenza. Vanno fissate dalla Fondazione prima, non dopo aver visto i risultati.")

bullets("Strumenti a basso codice", [
    "ChatGPT Business: GPT personalizzato o Progetto con la tassonomia come file. Zero codice",
    "Connettori: Make, Zapier, n8n, oppure le automazioni di Microsoft 365 o Google Workspace già in uso",
    "Il codice del repository serve quando volete misurare e integrare per davvero",
], notes="Non fare pubblicità a un fornitore. Il criterio: prendete lo strumento che qualcuno in Fondazione sa già usare.")

# ---------- 6. Esercitazione ----------
section("6. Esercitazione in gruppi", "20 minuti più 10 di restituzione", notes="Gruppi da 3-4. Griglia stampata in esercitazione/griglia_scomposizione.md.")

bullets("Consegna", [
    "Scegliete un processo della Fondazione: rendicontazione, rassegna stampa e bandi, iscrizioni, o uno vostro",
    "Scomponetelo con la griglia: un passo per riga, input, decisione, output",
    "Per ogni passo: integrazione, AI o umano?",
], notes="Insistere: un passo per riga anche se sembra banale. La banalità è dove si nascondono le integrazioni.")

image_full("La griglia, compilata sull'helpdesk", FIG + "griglia.png",
           caption="Tre passi su sette con AI. Due restano umani. Il resto è integrazione o regola.",
           notes="Esempio da usare come modello. Chiedere ai gruppi di arrivare a una tabella così.")

bullets("Restituzione: tre domande per gruppo", [
    "Qual è il passo che, automatizzato, fa risparmiare più tempo?",
    "Qual è il passo dove un errore del sistema costa di più?",
    "Quale numero misurereste dopo un mese per decidere se continuare?",
], notes="Due minuti a gruppo. Scrivere le risposte alla lavagna: di solito il passo che vale di più e quello che rischia di più sono vicini.")

bullets("Tre errori da evitare", [
    "Automatizzare prima di misurare",
    "Togliere l'umano troppo presto",
    "Comprare la piattaforma prima di aver definito il processo",
], notes="Chiusura. Sono le tre righe della tesi iniziale, al contrario.")

bullets("Materiali e contatti", [
    "Codice, dati, griglia e slide: github.com/<da completare>/promopa-agenti-ai",
    "Tutto gira anche senza chiave API (modalità 'mock') per provare la forma dell'output",
    "fabrizio.silvestri@uniroma1.it",
], notes="ATTENZIONE: il repository non è ancora pubblicato. Sostituire <da completare> con l'account GitHub prima della lezione, poi rigenerare il deck. Il comando di push è in HANDOFF.md.")

section("Grazie", "Domande?", notes="")

prs.save(OUT)
print("salvato", OUT, "slide:", len(prs.slides))
