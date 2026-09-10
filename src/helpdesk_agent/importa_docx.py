"""Importa gli esempi reali (anonimizzati) dal docx della Fondazione.

Il documento elenca le richieste numerate: un paragrafo che contiene solo
un numero apre una richiesta, tutto quello che segue le appartiene finché
non arriva il numero successivo. Le tabelle vengono lette nella posizione
in cui stanno nel documento, così il dettaglio dell'ordine resta attaccato
alla richiesta che lo contiene.

Lo script prova a riconoscere il canale da parole chiave e scrive
data/reali/richieste_reali.jsonl. Canale e mittente vanno poi controllati
a mano: è il primo esempio di "l'umano etichetta, il modello applica".

Uso:
    python -m helpdesk_agent.importa_docx "data/reali/Richieste a Promo PA Fondazione.docx"
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

from .schema import RADICE

CANALI = [
    ("zoom_chat", r"\bzoom\b|\bchat\b"),
    ("moodle_questionario", r"questionario|gradimento"),
    ("moodle_messaggio", r"\bmoodle\b"),
    ("form_sito", r"^oggetto:.*\bnome\b.*\bdescrizione\b|modulo di contatto"),
]

SEPARATORE = re.compile(r"^\d{1,2}$")


def indovina_canale(testo: str) -> str:
    """Prima ipotesi sul canale. Va confermata a mano, non è una verità."""
    t = re.sub(r"\s+", " ", testo.lower())
    for canale, pattern in CANALI:
        if re.search(pattern, t):
            return canale
    return "email"


def _blocchi_in_ordine(doc: Document) -> list[str]:
    """Paragrafi e tabelle nell'ordine in cui compaiono nel documento."""
    fuori = []
    for elemento in doc.element.body.iterchildren():
        if elemento.tag.endswith("}p"):
            fuori.append(Paragraph(elemento, doc).text.strip())
        elif elemento.tag.endswith("}tbl"):
            fuori.append(_tabella_a_testo(Table(elemento, doc)))
    return fuori


def _tabella_a_testo(tabella: Table) -> str:
    """Una riga per riga di tabella, nella forma 'campo: valore'."""
    righe = []
    for riga in tabella.rows:
        celle = []
        for cella in riga.cells:
            testo = cella.text.strip()
            if testo and (not celle or celle[-1] != testo):  # salta le celle unite
                celle.append(testo)
        if celle:
            righe.append(": ".join(celle))
    return "\n".join(righe)


def raggruppa(blocchi: list[str]) -> list[str]:
    """Unisce i blocchi in richieste, separandole sui paragrafi numerici."""
    richieste: list[list[str]] = []
    for blocco in blocchi:
        if not blocco:
            continue
        if SEPARATORE.match(blocco):
            richieste.append([])
        elif richieste:
            richieste[-1].append(blocco)
    return ["\n".join(r).strip() for r in richieste if r]


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    sorgente = Path(sys.argv[1])
    uscita = RADICE / "data" / "reali" / "richieste_reali.jsonl"
    uscita.parent.mkdir(parents=True, exist_ok=True)
    richieste = raggruppa(_blocchi_in_ordine(Document(str(sorgente))))
    with uscita.open("w", encoding="utf-8") as f:
        for i, testo in enumerate(richieste, 1):
            f.write(json.dumps(dict(
                id=f"RE{i:02d}", canale=indovina_canale(testo),
                sorgente="da verificare", mittente="da verificare", testo=testo,
            ), ensure_ascii=False) + "\n")
    print(f"Scritte {len(richieste)} richieste in {uscita}.")
    print("Ora controlla canale e mittente a mano: il docx non li dichiara.")


if __name__ == "__main__":
    main()
