"""Backend finto: regole a parole chiave.

Non è un classificatore serio ed è volutamente grezzo: serve a mostrare
la forma dell'output e a far girare la pipeline senza rete.
In aula il confronto tra mock e modello vero è un buon esempio di
"perché misuriamo".
"""
from __future__ import annotations

import re
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

_CORSI = [
    ("contratti-pubblici", r"contratt|affidament|cig\b"),
    ("digitalizzazione-pnrr", r"pnrr|digitalizz"),
    ("anticorruzione", r"anticorruz|trasparen"),
    ("privacy-gdpr", r"privacy|gdpr|trattament"),
    ("ia-pa", r"\bia\b|intelligenza|prompt|generativ"),
    ("bilancio-enti-locali", r"bilancio|contabil"),
]
_TIPI = [
    ("reclamo", r"terza volta|nessuna risposta|pessimo|lament"),
    ("attestato", r"attestat"),
    ("fatturazione", r"fattur|cig\b|split|pagament"),
    ("accesso-piattaforma", r"password|link zoom|non riesco|corrott|moodle|tentativi|audio"),
    ("iscrizione", r"iscri|sostitu|posti|doppione"),
    ("feedback", r"compliment|utile|concordo|ottimo|sarebbe utile|troppo veloce"),
    ("contenuti", r"slide|docente|materiale|riferiment|regolament|soglia"),
    ("informazioni", r"calendar|tariffa|interess|organizzate|edizione|newsletter"),
]
_OP = {
    "iscrizione": "segreteria-didattica", "attestato": "segreteria-didattica",
    "informazioni": "segreteria-didattica", "fatturazione": "amministrazione",
    "accesso-piattaforma": "tutor-piattaforma", "contenuti": "coordinamento-docenti",
    "reclamo": "direzione", "feedback": "direzione", "altro": "da-assegnare",
}


def _trova(regole, testo, default):
    t = testo.lower()
    for etichetta, pattern in regole:
        if re.search(pattern, t):
            return etichetta
    return default


def chiama(sistema: str, utente: str, schema: type[T]) -> T:
    nome = schema.__name__
    if nome == "Classificazione":
        return _classifica(utente, schema)
    if nome == "EstrazioneRisultato":
        return _estrai(utente, schema)
    if nome == "Bozza":
        return schema(testo="[mock] Gentile utente, grazie per la segnalazione. "
                            "La prendiamo in carico e la ricontattiamo a breve.\nSegreteria Promo PA")
    raise NotImplementedError(nome)


def _classifica(testo: str, schema):
    corso = _trova(_CORSI, testo, "nessuno")
    tipo = _trova(_TIPI, testo, "altro")
    t = testo.lower()
    if re.search(r"domani|tra un'ora|inizia tra|oggi|entro venerd", t):
        urg = "alta"
    elif tipo in ("feedback", "informazioni") or corso == "nessuno" and tipo == "altro":
        urg = "bassa"
    else:
        urg = "media"
    conf = 0.85 if (corso != "nessuno" and tipo != "altro") else 0.55
    return schema(corso=corso, tipologia=tipo, urgenza=urg, operatore=_OP[tipo],
                  confidenza=conf, campo_meno_sicuro="urgenza",
                  riassunto="[mock] " + testo.strip().split("\n")[-1][:80])


def _estrai(testo: str, schema):
    """Prende come richieste le righe che contengono un '?' o verbi di bisogno."""
    trovate = []
    for riga in testo.splitlines():
        r = riga.strip()
        if not r or r.startswith(("ISTRUZIONI", "TESTO")):
            continue
        m = re.match(r"\[(\d+:\d+)\]\s*([^:]+):\s*(.*)", r)
        if m:
            origine, mitt, corpo = m.group(1), m.group(2).strip(), m.group(3).strip()
        else:
            m2 = re.match(r"(Q\d+);(.*)", r)
            if not m2:
                continue
            origine, mitt, corpo = m2.group(1), "Anonimo", m2.group(2).strip()
        if "Promo PA" in mitt:
            continue
        if "?" in corpo or re.search(r"sarebbe utile|non ho ricevuto|avrei bisogno|troppo veloce|interesse", corpo, re.I):
            trovate.append(dict(id_origine=origine, mittente=mitt, testo=corpo,
                                motivazione="[mock] contiene una domanda o un bisogno esplicito"))
    return schema(richieste=trovate)
