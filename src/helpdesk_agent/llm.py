"""Chiamate al modello. Un solo punto di ingresso: `chiama(sistema, utente, Schema)`.

Due backend:
- "openai": Structured Outputs via Responses API. Il modello restituisce
  esattamente lo schema Pydantic richiesto, o un errore.
- "mock": regole a parole chiave. Non chiama nessuna API. Serve per
  provare la pipeline senza chiave e per far girare i test.

La scelta dipende da HELPDESK_BACKEND (default: openai se c'è OPENAI_API_KEY,
altrimenti mock).
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def _carica_env() -> None:
    """Legge un .env alla radice del repository, se c'e'.

    Le variabili gia' presenti nell'ambiente vincono: il file e' un comodo
    ripiego, non un modo per sovrascrivere quello che l'utente ha esportato.
    """
    percorso = Path(__file__).resolve().parents[2] / ".env"
    if not percorso.exists():
        return
    for riga in percorso.read_text(encoding="utf-8").splitlines():
        riga = riga.strip()
        if not riga or riga.startswith("#") or "=" not in riga:
            continue
        chiave, valore = riga.split("=", 1)
        os.environ.setdefault(chiave.strip(), valore.strip().strip('"').strip("'"))


_carica_env()

MODELLO_DEFAULT = os.environ.get("OPENAI_MODEL", "gpt-5-mini")


def backend() -> str:
    scelto = os.environ.get("HELPDESK_BACKEND")
    if scelto:
        return scelto
    return "openai" if os.environ.get("OPENAI_API_KEY") else "mock"


def chiama(sistema: str, utente: str, schema: type[T]) -> T:
    if backend() == "mock":
        from . import mock
        return mock.chiama(sistema, utente, schema)
    return _chiama_openai(sistema, utente, schema)


def _chiama_openai(sistema: str, utente: str, schema: type[T]) -> T:
    from openai import OpenAI

    client = OpenAI()
    risposta = client.responses.parse(
        model=MODELLO_DEFAULT,
        input=[
            {"role": "system", "content": sistema},
            {"role": "user", "content": utente},
        ],
        text_format=schema,
    )
    if risposta.output_parsed is None:
        raise RuntimeError(f"Il modello non ha prodotto un output valido: {risposta}")
    return risposta.output_parsed
