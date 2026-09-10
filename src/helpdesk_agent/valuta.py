"""Blocco 4: l'accuratezza si misura, non si stima.

Confronta le classificazioni prodotte con le etichette di riferimento
(data/etichette_oro.jsonl) e stampa accuratezza per campo, più la
percentuale di richieste che il sistema avrebbe assegnato da solo.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

CAMPI = ["corso", "tipologia", "urgenza", "operatore"]


def carica_jsonl(percorso: Path) -> list[dict]:
    return [json.loads(r) for r in percorso.read_text(encoding="utf-8").splitlines() if r.strip()]


def valuta(previsioni: list[dict], oro: list[dict]) -> dict:
    """previsioni: righe con id + campi; oro: righe con id + campi."""
    oro_per_id = {r["id"]: r for r in oro}
    corrette = Counter()
    totali = 0
    errori = defaultdict(list)
    automatiche = 0
    for p in previsioni:
        o = oro_per_id.get(p["id"])
        if o is None:
            continue
        totali += 1
        automatiche += int(p.get("assegnazione_automatica", False))
        for campo in CAMPI:
            if p[campo] == o[campo]:
                corrette[campo] += 1
            else:
                errori[campo].append((p["id"], o[campo], p[campo]))
    if totali == 0:
        return {"totali": 0}
    return {
        "totali": totali,
        "accuratezza": {c: round(corrette[c] / totali, 3) for c in CAMPI},
        "tutti_i_campi_corretti": round(
            sum(1 for p in previsioni if p["id"] in oro_per_id
                and all(p[c] == oro_per_id[p["id"]][c] for c in CAMPI)) / totali, 3),
        "quota_assegnazione_automatica": round(automatiche / totali, 3),
        "errori": dict(errori),
    }


def stampa(rapporto: dict) -> None:
    if rapporto.get("totali", 0) == 0:
        print("Nessuna richiesta valutabile.")
        return
    print(f"Richieste valutate: {rapporto['totali']}")
    for campo, acc in rapporto["accuratezza"].items():
        print(f"  {campo:12s} {acc:6.1%}")
    print(f"  {'tutti':12s} {rapporto['tutti_i_campi_corretti']:6.1%}")
    print(f"Assegnate automaticamente: {rapporto['quota_assegnazione_automatica']:.1%}")
    for campo, lista in rapporto["errori"].items():
        if lista:
            print(f"\nErrori su {campo} (id, atteso -> previsto):")
            for rid, atteso, previsto in lista:
                print(f"  {rid}: {atteso} -> {previsto}")
