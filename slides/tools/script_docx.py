"""Converte SCRIPT.md in SCRIPT.docx, formattato per essere letto mentre si parla.

Non e' un convertitore markdown generico: conosce le convenzioni di SCRIPT.md
e le rende in modo che, con l'occhio, si trovi subito la cosa che serve.

- "Dire" e' il parlato: corpo piu' grande, filetto blu a sinistra. E' quello
  che si legge davvero durante la lezione, quindi e' la cosa piu' visibile.
- "Fare" e' un'azione: corsivo grigio con un triangolino davanti.
- I titoli di slide hanno una fascia azzurra: sfogliando si trova il punto.
- I blocchi di codice sono su fondo grigio, in monospazio, e non vanno a capo.

Uso:
    python slides/tools/script_docx.py
"""
from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

SORGENTE = Path("SCRIPT.md")
USCITA = Path("SCRIPT.docx")

BLU = RGBColor(0x1B, 0x3A, 0x5F)
BORD = RGBColor(0x82, 0x24, 0x33)
NERO = RGBColor(0x1A, 0x1A, 0x1A)
GRIG = RGBColor(0x5A, 0x5A, 0x5A)
AZZURRO = "E8EEF5"
GRIGINO = "F2F2F2"

TESTO = "Calibri"        # c'e' su Word, e LibreOffice lo sostituisce con Carlito
MONO = "Consolas"


def _famiglia(oggetto, nome: str) -> None:
    """Imposta il carattere su tutte le varianti, non solo su quella latina.

    Senza questo, chi apre il file con un lettore che non ha il font ricade
    sul Times del documento e tutto lo script diventa un tema di terza media.
    """
    rPr = oggetto.element.get_or_add_rPr() if hasattr(oggetto, "element") else None
    if rPr is None:
        return
    rf = rPr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts"); rPr.append(rf)
    for attributo in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(attributo), nome)


# --- mattoni XML che python-docx non espone -----------------------------

def _sfondo(par, colore: str) -> None:
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), colore)
    par._p.get_or_add_pPr().append(shd)


def _bordo(par, lato: str, colore: str, spessore: int = 18, spazio: int = 8) -> None:
    pPr = par._p.get_or_add_pPr()
    bdr = pPr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr"); pPr.append(bdr)
    e = OxmlElement(f"w:{lato}")
    e.set(qn("w:val"), "single"); e.set(qn("w:sz"), str(spessore))
    e.set(qn("w:space"), str(spazio)); e.set(qn("w:color"), colore)
    bdr.append(e)


def _non_spezzare(par) -> None:
    """Tiene il paragrafo con il successivo: i titoli non restano orfani."""
    pPr = par._p.get_or_add_pPr()
    for tag in ("w:keepNext", "w:keepLines"):
        pPr.append(OxmlElement(tag))


def _numeri_di_pagina(sezione) -> None:
    par = sezione.footer.paragraphs[0]
    par.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = par.add_run("Script della lezione, 15 settembre 2026    ")
    r.font.size = Pt(8); r.font.color.rgb = GRIG; r.font.name = TESTO; _famiglia(r, TESTO)
    for pezzo, testo in (("begin", None), (None, "PAGE"), ("end", None)):
        e = OxmlElement("w:r")
        if pezzo:
            f = OxmlElement("w:fldChar"); f.set(qn("w:fldCharType"), pezzo); e.append(f)
        else:
            i = OxmlElement("w:instrText"); i.set(qn("xml:space"), "preserve")
            i.text = f" {testo} "; e.append(i)
        par._p.append(e)


# --- testo con grassetto e monospazio in linea --------------------------

INLINE = re.compile(r"(\*\*.+?\*\*|`[^`]+`)")
# una riga che comincia cosi' apre qualcosa di nuovo: il paragrafo precedente
# finisce qui. Il rientro va ammesso, perche' gli elenchi annidano.
NUOVO_BLOCCO = re.compile(r"^\s*(#|\*\*|-\s|\d+\.\s|\||```|---)")


def _scrivi(par, testo: str, size: float, colore=NERO, corsivo=False, bold=False) -> None:
    for pezzo in INLINE.split(testo):
        if not pezzo:
            continue
        r = par.add_run()
        if pezzo.startswith("**") and pezzo.endswith("**"):
            r.text = pezzo[2:-2]; r.font.bold = True; r.font.name = TESTO; _famiglia(r, TESTO)
        elif pezzo.startswith("`") and pezzo.endswith("`"):
            r.text = pezzo[1:-1]; r.font.name = MONO; _famiglia(r, MONO); r.font.size = Pt(size - 1.5)
            r.font.color.rgb = BORD
            continue
        else:
            r.text = pezzo; r.font.bold = bold; r.font.name = TESTO; _famiglia(r, TESTO)
        r.font.size = Pt(size); r.font.color.rgb = colore; r.font.italic = corsivo


# --- i tipi di paragrafo dello script -----------------------------------

def blocco_titolo(doc, testo: str, primo: bool) -> None:
    if not primo:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run(testo)
    r.font.size = Pt(21); r.font.bold = True; r.font.color.rgb = BLU; r.font.name = TESTO; _famiglia(r, TESTO)
    _bordo(p, "bottom", "1B3A5F", spessore=12, spazio=6)
    _non_spezzare(p)


def slide_titolo(doc, numero: str, titolo: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16); p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(-0.2)
    r = p.add_run(f"  SLIDE {numero}   ")
    r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = BORD; r.font.name = TESTO; _famiglia(r, TESTO)
    r = p.add_run(titolo + "  ")
    r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = BLU; r.font.name = TESTO; _famiglia(r, TESTO)
    _sfondo(p, AZZURRO)
    _non_spezzare(p)


def sotto_titolo(doc, testo: str, livello: int) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14 if livello == 2 else 10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(testo)
    r.font.size = Pt(14 if livello == 2 else 12)
    r.font.bold = True; r.font.color.rgb = BLU; r.font.name = TESTO; _famiglia(r, TESTO)
    _non_spezzare(p)


def paragrafo_dire(doc, etichetta: str, testo: str) -> None:
    """Il parlato: e' la cosa che si legge davvero, quindi e' la piu' visibile."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.55)
    p.paragraph_format.space_before = Pt(7); p.paragraph_format.space_after = Pt(7)
    p.paragraph_format.line_spacing = 1.22
    r = p.add_run(etichetta + " ")
    r.font.size = Pt(10.5); r.font.bold = True; r.font.color.rgb = BORD
    r.font.all_caps = True; r.font.name = TESTO; _famiglia(r, TESTO)
    _scrivi(p, testo, 12.5)
    _bordo(p, "left", "1B3A5F", spessore=20, spazio=10)


def paragrafo_fare(doc, etichetta: str, testo: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.55)
    p.paragraph_format.space_before = Pt(5); p.paragraph_format.space_after = Pt(5)
    r = p.add_run("▸ ")
    r.font.size = Pt(11); r.font.color.rgb = GRIG; r.font.name = TESTO; _famiglia(r, TESTO)
    r = p.add_run(etichetta + " ")
    r.font.size = Pt(10); r.font.bold = True; r.font.color.rgb = GRIG
    r.font.all_caps = True; r.font.name = TESTO; _famiglia(r, TESTO)
    _scrivi(p, testo, 11, colore=GRIG, corsivo=True)


def paragrafo_semplice(doc, testo: str) -> None:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    _scrivi(p, testo, 11)


def elenco(doc, testo: str, numerato: bool, rientro: int = 0) -> None:
    p = doc.add_paragraph(style="List Number" if numerato else "List Bullet")
    p.paragraph_format.left_indent = Cm(0.9 + rientro * 0.6)
    p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
    _scrivi(p, testo, 11)


def codice(doc, righe: list[str]) -> None:
    for i, riga in enumerate(righe):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(0.55)
        p.paragraph_format.space_before = Pt(6 if i == 0 else 0)
        p.paragraph_format.space_after = Pt(6 if i == len(righe) - 1 else 0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(riga or " ")
        r.font.name = MONO; _famiglia(r, MONO); r.font.size = Pt(9); r.font.color.rgb = NERO
        _sfondo(p, GRIGINO)
        if i == 0:
            _bordo(p, "top", "D8D8D8", spessore=6, spazio=2)
        if i == len(righe) - 1:
            _bordo(p, "bottom", "D8D8D8", spessore=6, spazio=2)
        _bordo(p, "left", "D8D8D8", spessore=6, spazio=6)
        _bordo(p, "right", "D8D8D8", spessore=6, spazio=6)


def tabella(doc, righe: list[list[str]]) -> None:
    t = doc.add_table(rows=0, cols=len(righe[0]))
    t.style = "Table Grid"
    t.autofit = False
    # senza layout fisso Word ricalcola le colonne a modo suo e le larghezze
    # che impostiamo qui sotto vengono ignorate
    tblPr = t._tbl.tblPr
    layout = OxmlElement("w:tblLayout"); layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    larghezze = ([Cm(1.1), Cm(7.3), Cm(2.6), Cm(5.6)] if len(righe[0]) == 4
                 else [Cm(16.6 / len(righe[0]))] * len(righe[0]))
    grid = t._tbl.find(qn("w:tblGrid"))
    for col, larghezza in zip(grid.findall(qn("w:gridCol")), larghezze):
        col.set(qn("w:w"), str(int(larghezza.twips)))
    for i, riga in enumerate(righe):
        riga_doc = t.add_row()
        # una riga non si spezza mai fra due pagine
        riga_doc._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        celle = riga_doc.cells
        for c, valore, larghezza in zip(celle, riga, larghezze):
            c.width = larghezza
            c.text = ""
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(3)
            _scrivi(p, valore, 10, colore=RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else NERO,
                    bold=(i == 0))
            if i == 0:
                _sfondo(p, "1B3A5F")
                tcPr = c._tc.get_or_add_tcPr()
                shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear")
                shd.set(qn("w:fill"), "1B3A5F"); tcPr.append(shd)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)


# --- copertina ----------------------------------------------------------

def copertina(doc) -> None:
    for _ in range(4):
        doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Script della lezione")
    r.font.size = Pt(30); r.font.bold = True; r.font.color.rgb = BLU; r.font.name = TESTO; _famiglia(r, TESTO)
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Agenti AI per i processi interni")
    r.font.size = Pt(16); r.font.color.rgb = BORD; r.font.name = TESTO; _famiglia(r, TESTO)
    doc.add_paragraph()
    for riga in ("Promo PA Fondazione", "15 settembre 2026, da remoto, due ore",
                 "Cento slide", "Fabrizio Silvestri, Sapienza Università di Roma, DIAG"):
        p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(riga); r.font.size = Pt(12); r.font.color.rgb = GRIG; r.font.name = TESTO; _famiglia(r, TESTO)
    doc.add_paragraph()
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("Generato da SCRIPT.md. Non modificare questo file a mano:\n"
                  "si cambia SCRIPT.md e si rilancia slides/tools/script_docx.py")
    r.font.size = Pt(9); r.font.italic = True; r.font.color.rgb = GRIG; r.font.name = TESTO; _famiglia(r, TESTO)
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


# --- il ciclo principale ------------------------------------------------

ETICHETTE_DIRE = ("dire", "mentre elabora", "quando risponde", "poi dire", "e poi",
                  "quando finisce", "e questa e", "dire, e questa")
SLIDE = re.compile(r"^## Slide (\d+)\. (.+)$")
GRASSETTO_INIZIALE = re.compile(r"^\*\*([^*]+?):\*\*\s*(.*)$")
CLIC = re.compile(r"^\*\*\[clic\]\*\*\s*(.*)$")


def converti() -> None:
    testo = SORGENTE.read_text(encoding="utf-8").splitlines()
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21), Cm(29.7)
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin = Cm(2.0); s.bottom_margin = Cm(1.8)
    _numeri_di_pagina(s)
    stile = doc.styles["Normal"]
    stile.font.size = Pt(11)
    stile.font.name = TESTO
    rf = stile.element.rPr.rFonts
    for attributo in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rf.set(qn(attributo), TESTO)

    copertina(doc)

    i, primo_blocco = 0, True
    while i < len(testo):
        riga = testo[i].rstrip()

        if riga.lstrip().startswith("```"):
            chiuse = []
            i += 1
            rientro_fence = len(testo[i - 1]) - len(testo[i - 1].lstrip())
            while i < len(testo) and not testo[i].lstrip().startswith("```"):
                chiuse.append(testo[i][rientro_fence:].rstrip("\n")); i += 1
            codice(doc, chiuse)
            i += 1
            continue

        if riga.startswith("|") and riga.endswith("|"):
            blocco = []
            while i < len(testo) and testo[i].startswith("|"):
                celle = [c.strip() for c in testo[i].strip().strip("|").split("|")]
                if not all(set(c) <= set("-: ") for c in celle):
                    blocco.append(celle)
                i += 1
            if blocco:
                tabella(doc, blocco)
            continue

        if not riga or riga == "---":
            i += 1
            continue

        if riga.startswith("# "):
            blocco_titolo(doc, riga[2:], primo_blocco); primo_blocco = False
        elif (m := SLIDE.match(riga)):
            slide_titolo(doc, m.group(1), m.group(2))
        elif riga.startswith("## "):
            sotto_titolo(doc, riga[3:], 2)
        elif riga.startswith("### "):
            sotto_titolo(doc, riga[4:], 3)
        elif riga.startswith("- ") or riga.startswith("   - ") or re.match(r"^\d+\. ", riga):
            rientro = 1 if riga.startswith("   - ") else 0
            numerato = bool(re.match(r"^\d+\. ", riga))
            corpo = (riga.split(". ", 1)[1] if numerato
                     else riga.strip()[2:])
            # le righe indentate sotto un punto elenco sono la sua continuazione
            while i + 1 < len(testo) and testo[i + 1].strip() and not NUOVO_BLOCCO.match(testo[i + 1]):
                i += 1
                corpo += " " + testo[i].strip()
            elenco(doc, corpo, numerato=numerato, rientro=rientro)
        elif (m := CLIC.match(riga)) and m.group(1):
            resto = m.group(1)
            while i + 1 < len(testo) and testo[i + 1].strip() and not NUOVO_BLOCCO.match(testo[i + 1]):
                i += 1
                resto += " " + testo[i].strip()
            paragrafo_dire(doc, "[clic]", resto)
        elif (m := GRASSETTO_INIZIALE.match(riga)) and m.group(2):
            etichetta, resto = m.group(1), m.group(2)
            # le righe che continuano sotto fanno parte dello stesso paragrafo
            while i + 1 < len(testo) and testo[i + 1].strip() and not NUOVO_BLOCCO.match(testo[i + 1]):
                i += 1
                resto += " " + testo[i].strip()
            if any(etichetta.lower().startswith(e) for e in ETICHETTE_DIRE):
                paragrafo_dire(doc, etichetta + ":", resto)
            else:
                paragrafo_fare(doc, etichetta + ":", resto)
        else:
            corpo = riga
            while i + 1 < len(testo) and testo[i + 1].strip() and not NUOVO_BLOCCO.match(testo[i + 1]):
                i += 1
                corpo += " " + testo[i].strip()
            paragrafo_semplice(doc, corpo)
        i += 1

    doc.save(USCITA)
    print(f"salvato {USCITA} ({USCITA.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    converti()
