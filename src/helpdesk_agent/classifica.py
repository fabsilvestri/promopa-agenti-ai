"""Esigenza 3: classificare per corso, tipologia, urgenza, stato, operatore.

Pattern: routing con output strutturato.
- La tassonomia arriva dal file YAML, non è scritta nel prompt a mano.
- Il modello restituisce un oggetto `Classificazione`, mai testo libero.
- Sotto la soglia di confidenza l'assegnazione automatica si ferma e la
  richiesta resta a un umano. Questo è il punto di controllo.
"""
from __future__ import annotations

from .llm import chiama
from .schema import TASSONOMIA, Classificazione, Richiesta, RichiestaClassificata, tassonomia_per_prompt

SISTEMA = f"""Sei il sistema di smistamento dell'helpdesk formazione di Promo PA Fondazione,
che eroga corsi per dipendenti della pubblica amministrazione.

Classifica ogni richiesta usando SOLO le voci di questa tassonomia:

{tassonomia_per_prompt()}

Regole:
- Scegli l'operatore coerente con la tipologia (vedi competenze).
- Un reclamo esplicito (tono di lamentela, solleciti ripetuti) prevale sulla
  tipologia dell'oggetto: va a "reclamo" e alla direzione.
- Urgenza alta solo se c'è un vincolo di tempo esplicito o un blocco
  (corso oggi o domani, accesso negato, minaccia di escalation).
- Se il corso non è chiaro usa "nessuno". Non indovinare.
- La confidenza è la tua stima onesta: se un campo è ambiguo, abbassala e
  indicalo in `campo_meno_sicuro`.
- Il riassunto è per l'operatore: chi chiede cosa, in una riga.
"""


def classifica(richiesta: Richiesta) -> RichiestaClassificata:
    utente = (
        f"CANALE: {richiesta.canale}\nSORGENTE: {richiesta.sorgente}\n"
        f"MITTENTE: {richiesta.mittente}\nTESTO:\n{richiesta.testo}"
    )
    c: Classificazione = chiama(SISTEMA, utente, Classificazione)
    automatica = c.confidenza >= TASSONOMIA["soglia_confidenza"]
    return RichiestaClassificata(
        richiesta=richiesta,
        classificazione=c,
        stato="nuova",
        assegnazione_automatica=automatica,
    )
