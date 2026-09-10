"""Pipeline completa: ingestione -> estrazione -> classificazione -> bozze -> report.

Questo è un WORKFLOW, non un agente autonomo: i passi li decidiamo noi.
L'AI sta dentro due passi (estrazione e classificazione) e in uno opzionale
(bozze). Tutto il resto è integrazione e tabelle.

Uso:
    python -m helpdesk_agent.pipeline --bozze --out demo/output
    HELPDESK_BACKEND=mock python -m helpdesk_agent.pipeline
"""
from __future__ import annotations

import argparse
import csv
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from .bozza import scrivi_bozza
from .classifica import classifica
from .estrai import estrai_moodle_questionario, estrai_zoom
from .llm import backend
from .schema import RADICE, Richiesta, RichiestaClassificata
from .valuta import carica_jsonl, stampa, valuta

DATI = RADICE / "data"


def ingerisci() -> list[Richiesta]:
    """Passo 1: repository unico. Qui è un file; in produzione un ticketing."""
    righe = carica_jsonl(DATI / "richieste.jsonl")
    return [Richiesta(**r) for r in righe]


def estrai_grezzi() -> list[Richiesta]:
    """Passo 2: i canali che oggi si perdono."""
    trovate = []
    zoom = DATI / "grezzi" / "zoom_chat_contratti_2026-09-03.txt"
    if zoom.exists():
        trovate += estrai_zoom(zoom, "corso: Codice contratti, 2026-09-03")
    moodle = DATI / "grezzi" / "moodle_questionario_privacy.csv"
    if moodle.exists():
        trovate += estrai_moodle_questionario(moodle, "corso: Privacy e GDPR")
    return trovate


def riga_csv(rc: RichiestaClassificata) -> dict:
    c = rc.classificazione
    return dict(
        id=rc.richiesta.id, canale=rc.richiesta.canale, mittente=rc.richiesta.mittente,
        corso=c.corso.value, tipologia=c.tipologia.value, urgenza=c.urgenza,
        operatore=c.operatore.value, stato=rc.stato,
        confidenza=c.confidenza, assegnazione_automatica=rc.assegnazione_automatica,
        riassunto=c.riassunto, testo=rc.richiesta.testo,
        bozza_risposta=rc.bozza_risposta or "",
    )


def scrivi_report(righe: list[dict], cartella: Path) -> None:
    cartella.mkdir(parents=True, exist_ok=True)
    with (cartella / "richieste_classificate.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(righe[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(righe)
    with (cartella / "richieste_classificate.jsonl").open("w", encoding="utf-8") as f:
        for r in righe:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # Vista per operatore: quello che ognuno vedrebbe la mattina.
    md = ["# Coda helpdesk formazione\n"]
    for op in sorted({r["operatore"] for r in righe}):
        md.append(f"\n## {op}\n")
        for r in sorted((x for x in righe if x["operatore"] == op),
                        key=lambda x: {"alta": 0, "media": 1, "bassa": 2}[x["urgenza"]]):
            flag = "" if r["assegnazione_automatica"] else " (DA VERIFICARE, confidenza bassa)"
            md.append(f"- [{r['urgenza'].upper()}] {r['id']} · {r['tipologia']} · {r['corso']}{flag}\n"
                      f"  {r['riassunto']}")
    (cartella / "coda_per_operatore.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bozze", action="store_true", help="genera anche le bozze di risposta")
    ap.add_argument("--senza-grezzi", action="store_true", help="salta l'estrazione da Zoom e Moodle")
    ap.add_argument("--solo-grezzi", action="store_true",
                    help="solo Zoom e Moodle: e' la parte che si vede meglio in demo")
    ap.add_argument("--limite", type=int, default=0,
                    help="ferma dopo N richieste. In aula serve: quaranta richieste con "
                         "le bozze sono venticinque minuti, cinque sono un minuto")
    ap.add_argument("--paralleli", type=int, default=6,
                    help="quante richieste in parallelo. Con 1 le righe escono una alla "
                         "volta, piu' lento ma piu' bello da guardare in aula")
    ap.add_argument("--out", default=str(RADICE / "demo" / "output"))
    args = ap.parse_args()

    print(f"Backend: {backend()}")
    richieste = [] if args.solo_grezzi else ingerisci()
    print(f"Richieste strutturate: {len(richieste)}")
    if not args.senza_grezzi:
        estratte = estrai_grezzi()
        print(f"Richieste estratte da Zoom e Moodle: {len(estratte)}")
        richieste += estratte
    if args.limite:
        richieste = richieste[:args.limite]
        print(f"Limite attivo: mi fermo a {len(richieste)} richieste")

    def lavora(r: Richiesta) -> RichiestaClassificata:
        rc = classifica(r)
        if args.bozze:
            rc.bozza_risposta = scrivi_bozza(rc)
        return rc

    # Le richieste sono indipendenti fra loro: in fila sono tredici secondi
    # l'una, in parallelo il tempo e' quello della piu' lenta. Le righe si
    # stampano comunque in ordine, cosi' in aula si legge come una lista.
    if args.paralleli > 1:
        with ThreadPoolExecutor(max_workers=args.paralleli) as pool:
            classificate = list(pool.map(lavora, richieste))
    else:
        classificate = [lavora(r) for r in richieste]
    for r, rc in zip(richieste, classificate):
        segno = "auto" if rc.assegnazione_automatica else "UMANO"
        print(f"  {r.id:8s} {rc.classificazione.tipologia.value:20s} -> {rc.classificazione.operatore.value:22s} [{segno}]")

    righe = [riga_csv(rc) for rc in classificate]
    scrivi_report(righe, Path(args.out))
    print(f"\nReport in {args.out}/")

    oro = carica_jsonl(DATI / "etichette_oro.jsonl")
    print("\nValutazione contro le etichette di riferimento:")
    stampa(valuta(righe, oro))


if __name__ == "__main__":
    main()
