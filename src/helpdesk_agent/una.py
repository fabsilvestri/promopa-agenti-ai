"""Classifica una sola richiesta, per la demo dal vivo.

Serve al momento in cui qualcuno in aula detta una richiesta e si vuole
vedere cosa ne fa il sistema, senza rilanciare tutta la pipeline.

Uso:
    cd src
    python -m helpdesk_agent.una "Non riesco a scaricare l'attestato del corso di ieri"
    python -m helpdesk_agent.una --bozza "..."          # aggiunge la bozza di risposta
    python -m helpdesk_agent.una                        # legge il testo da tastiera

Senza OPENAI_API_KEY parte da sola in modalita' mock: risponde comunque,
con regole a parole chiave, e lo dice.
"""
from __future__ import annotations

import argparse
import sys

from .bozza import scrivi_bozza
from .classifica import classifica
from .llm import backend
from .schema import TASSONOMIA, Richiesta


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("testo", nargs="*", help="il testo della richiesta")
    ap.add_argument("--bozza", action="store_true", help="scrivi anche la bozza di risposta")
    ap.add_argument("--canale", default="email", help="email, form_sito, moodle_messaggio, zoom_chat")
    ap.add_argument("--mittente", default="Partecipante in aula")
    args = ap.parse_args()

    testo = " ".join(args.testo).strip()
    if not testo:
        print("Scrivi la richiesta e premi invio due volte.\n")
        testo = sys.stdin.read().strip()
    if not testo:
        print("Nessun testo, nessuna classificazione.")
        sys.exit(1)

    print(f"\nBackend: {backend()}   soglia: {TASSONOMIA['soglia_confidenza']}")
    print("-" * 66)
    richiesta = Richiesta(id="LIVE", canale=args.canale, sorgente="demo in aula",
                          mittente=args.mittente, testo=testo)
    rc = classifica(richiesta)
    c = rc.classificazione

    print(f"corso              {c.corso.value}")
    print(f"tipologia          {c.tipologia.value}")
    print(f"urgenza            {c.urgenza}")
    print(f"operatore          {c.operatore.value}")
    print(f"confidenza         {c.confidenza:.2f}")
    print(f"campo meno sicuro  {c.campo_meno_sicuro}")
    print(f"riassunto          {c.riassunto}")
    print("-" * 66)
    if rc.assegnazione_automatica:
        print(f"ASSEGNATA in automatico a {c.operatore.value}")
    else:
        print("SOTTO SOGLIA: nessuna assegnazione, va in coda da verificare")

    if args.bozza:
        print("\nBozza di risposta:\n")
        print(scrivi_bozza(rc))


if __name__ == "__main__":
    main()
