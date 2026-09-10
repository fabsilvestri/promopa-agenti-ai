"""Schemi dei dati. Il modello produce SOLO oggetti di questa forma.

Il punto didattico: la tassonomia vive qui e in data/tassonomia.yaml,
non nel prompt. Cambiare un corso o un operatore non richiede di riscrivere
il prompt.
"""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field

RADICE = Path(__file__).resolve().parents[2]
TASSONOMIA = yaml.safe_load((RADICE / "data" / "tassonomia.yaml").read_text(encoding="utf-8"))

Corso = Enum("Corso", {c["id"].replace("-", "_"): c["id"] for c in TASSONOMIA["corsi"]}, type=str)
Tipologia = Enum("Tipologia", {t["id"].replace("-", "_"): t["id"] for t in TASSONOMIA["tipologie"]}, type=str)
Operatore = Enum("Operatore", {o["id"].replace("-", "_"): o["id"] for o in TASSONOMIA["operatori"]}, type=str)
Urgenza = Literal["alta", "media", "bassa"]
Canale = Literal["email", "form_sito", "moodle_messaggio", "moodle_questionario", "zoom_chat"]


class Richiesta(BaseModel):
    """Una richiesta grezza, prima della classificazione."""
    id: str
    canale: Canale
    sorgente: str = Field(description="Casella e-mail, pagina del sito, corso Moodle o sessione Zoom")
    mittente: str = "Sconosciuto"
    testo: str


class RichiestaEstratta(BaseModel):
    """Una richiesta trovata dentro testo non strutturato (chat Zoom, questionario)."""
    id_origine: str = Field(description="Riga o risposta da cui è stata estratta")
    mittente: str
    testo: str = Field(description="La richiesta, riportata con le parole dell'utente")
    motivazione: str = Field(description="Perché è una richiesta e non rumore, in una frase")


class EstrazioneRisultato(BaseModel):
    richieste: list[RichiestaEstratta]


class Classificazione(BaseModel):
    """Output strutturato del classificatore. Ogni campo ha una confidenza."""
    corso: Corso
    tipologia: Tipologia
    urgenza: Urgenza
    operatore: Operatore
    confidenza: float = Field(ge=0, le=1, description="Confidenza complessiva, 0-1")
    campo_meno_sicuro: str = Field(description="Il campo su cui il modello è meno sicuro")
    riassunto: str = Field(description="Una riga per l'operatore, massimo 20 parole")


class RichiestaClassificata(BaseModel):
    richiesta: Richiesta
    classificazione: Classificazione
    stato: Literal["nuova", "presa-in-carico", "in-attesa-utente", "chiusa"] = "nuova"
    assegnazione_automatica: bool
    bozza_risposta: str | None = None


def schema_json(modello: type[BaseModel]) -> dict:
    """Schema JSON da passare al modello (Structured Outputs)."""
    return modello.model_json_schema()


def tassonomia_per_prompt() -> str:
    """Rende la tassonomia leggibile dal modello."""
    righe = ["CORSI:"]
    righe += [f"- {c['id']}: {c['nome']}" for c in TASSONOMIA["corsi"]]
    righe.append("TIPOLOGIE:")
    righe += [f"- {t['id']}: {t['descrizione']}" for t in TASSONOMIA["tipologie"]]
    righe.append("URGENZA:")
    righe += [f"- {u['id']}: {u['descrizione']}" for u in TASSONOMIA["urgenza"]]
    righe.append("OPERATORI (ruolo -> tipologie di competenza):")
    righe += [f"- {o['id']}: {', '.join(o['competenze'])}" for o in TASSONOMIA["operatori"]]
    return "\n".join(righe)
