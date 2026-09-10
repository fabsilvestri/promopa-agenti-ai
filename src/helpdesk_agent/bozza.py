"""Esigenza 4 (parte AI): bozze di risposta.

Il modello scrive, l'operatore invia. La bozza non deve inventare
informazioni che il sistema non ha (date, importi, numeri di protocollo):
dove servono, lascia un segnaposto tra parentesi quadre.
"""
from __future__ import annotations

from pydantic import BaseModel, Field

from .llm import chiama
from .schema import RichiestaClassificata


class Bozza(BaseModel):
    testo: str = Field(description="Bozza di risposta pronta da rivedere e inviare")


SISTEMA = """Scrivi bozze di risposta per l'helpdesk formazione di Promo PA Fondazione.

Stile: italiano professionale, cordiale, breve. Del Lei. Firma "Segreteria Promo PA".
Regole:
- Rispondi solo a ciò che è stato chiesto.
- Non inventare date, importi, nomi, numeri di fattura o procedure. Se
  servono, usa un segnaposto tra parentesi quadre, es. [data], [importo].
- Se la richiesta è un reclamo, riconosci il disagio in una frase, senza
  giustificazioni, e indica un passo concreto.
- Se la richiesta non è di tua competenza o è ambigua, scrivi una bozza che
  chiede l'informazione mancante.
- Massimo 120 parole.
"""


def scrivi_bozza(rc: RichiestaClassificata) -> str:
    c = rc.classificazione
    utente = (
        f"RICHIESTA ({rc.richiesta.canale}, da {rc.richiesta.mittente}):\n{rc.richiesta.testo}\n\n"
        f"CLASSIFICAZIONE: corso={c.corso.value}, tipologia={c.tipologia.value}, "
        f"urgenza={c.urgenza}, operatore={c.operatore.value}\n"
        f"NOTA: {c.riassunto}"
    )
    return chiama(SISTEMA, utente, Bozza).testo
