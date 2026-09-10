"""Esigenza 2: recuperare richieste da testo non strutturato.

Chat Zoom e risposte aperte dei questionari Moodle non sono richieste:
sono testo in cui QUALCHE riga è una richiesta. Il compito del modello
è separare il segnale dal rumore e riportare la richiesta con le parole
dell'utente, senza riscriverla.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

from .llm import chiama
from .schema import EstrazioneRisultato, Richiesta

SISTEMA = """Sei l'assistente dell'helpdesk formazione di Promo PA Fondazione.
Ricevi testo non strutturato: la chat di un corso su Zoom oppure le risposte
aperte di un questionario di gradimento.

Estrai SOLO le righe che contengono una richiesta rivolta alla Fondazione:
una domanda, un problema da risolvere, un bisogno (materiale mancante,
attestato, informazioni), una proposta o una lamentela su cui qualcuno
dovrebbe agire.

Ignora: saluti, conferme, ringraziamenti generici, messaggi della Segreteria,
problemi che l'utente dichiara già risolti.

Regole:
- Riporta il testo con le parole dell'utente. Non riassumere, non correggere.
- Se una riga si associa a una richiesta precedente ("mi associo"), non
  creare una nuova richiesta.
- Per ogni richiesta spiega in una frase perché è una richiesta.
- In `id_origine` scrivi SOLO l'identificativo della riga: per la chat
  l'orario nella forma hh:mm, per il questionario l'id della risposta.
  Niente nome del mittente, niente parentesi quadre, niente altro testo.
"""

ORARIO = re.compile(r"(\d{1,2}):(\d{2})")
NON_ALFANUMERICI = re.compile(r"[^0-9A-Za-z]")


def _id_chat(grezzo: str) -> str:
    """Dall'id_origine ricava l'orario, in forma hhmm.

    Il modello tende a riportare l'intera riga, "[10:11] Comune di Pisa - L.R.",
    anche quando il prompt chiede solo l'orario. L'identificativo di una
    richiesta non può dipendere da come il modello si sente quel giorno:
    lo ricostruiamo noi.
    """
    trovato = ORARIO.search(grezzo)
    if trovato:
        return f"{int(trovato.group(1)):02d}{trovato.group(2)}"
    return NON_ALFANUMERICI.sub("", grezzo)[:12] or "ignoto"


def _id_questionario(grezzo: str) -> str:
    """Per il questionario l'id della risposta è già univoco."""
    return NON_ALFANUMERICI.sub("", grezzo)[:12] or "ignoto"


def estrai_da_testo(testo: str, canale: str, sorgente: str, prefisso_id: str,
                    pulisci_id=_id_chat) -> list[Richiesta]:
    utente = f"TESTO ({sorgente}):\n{testo}"
    risultato = chiama(SISTEMA, utente, EstrazioneRisultato)
    return [
        Richiesta(
            id=f"{prefisso_id}-{pulisci_id(r.id_origine)}",
            canale=canale,
            sorgente=sorgente,
            mittente=r.mittente,
            testo=r.testo,
        )
        for r in risultato.richieste
    ]


def estrai_zoom(percorso: Path, sorgente: str) -> list[Richiesta]:
    return estrai_da_testo(percorso.read_text(encoding="utf-8"), "zoom_chat", sorgente, "Z")


def estrai_moodle_questionario(percorso: Path, sorgente: str) -> list[Richiesta]:
    with percorso.open(encoding="utf-8") as f:
        righe = list(csv.DictReader(f, delimiter=";"))
    testo = "\n".join(f"{r['id']};{r['risposta_aperta']}" for r in righe)
    richieste = estrai_da_testo(testo, "moodle_questionario", sorgente, "Q",
                                pulisci_id=_id_questionario)
    # Gli id delle risposte portano già la Q: "Q-Q02" diventa "Q02".
    for r in richieste:
        r.id = r.id.replace("Q-Q", "Q")
    return richieste
