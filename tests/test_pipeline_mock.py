"""Test con backend mock: nessuna chiamata di rete."""
import os

os.environ["HELPDESK_BACKEND"] = "mock"

from helpdesk_agent.classifica import classifica  # noqa: E402
from helpdesk_agent.estrai import estrai_zoom  # noqa: E402
from helpdesk_agent.schema import RADICE, TASSONOMIA, Richiesta  # noqa: E402
from helpdesk_agent.valuta import carica_jsonl, valuta  # noqa: E402


def test_tassonomia_coerente():
    tipologie = {t["id"] for t in TASSONOMIA["tipologie"]}
    coperte = {c for o in TASSONOMIA["operatori"] for c in o["competenze"]}
    assert tipologie == coperte, "ogni tipologia deve avere un operatore"


def test_classifica_restituisce_schema_valido():
    r = Richiesta(id="T1", canale="email", sorgente="formazione@", mittente="x",
                  testo="Non ho ricevuto il link Zoom del corso di domani")
    rc = classifica(r)
    assert rc.classificazione.tipologia.value == "accesso-piattaforma"
    assert rc.classificazione.urgenza == "alta"
    assert 0 <= rc.classificazione.confidenza <= 1


def test_estrazione_scarta_rumore():
    trovate = estrai_zoom(RADICE / "data" / "grezzi" / "zoom_chat_contratti_2026-09-03.txt", "test")
    testi = " ".join(t.testo for t in trovate)
    assert "attestato" in testi
    assert "buongiorno" not in testi.lower()


def test_valutazione_formato():
    oro = carica_jsonl(RADICE / "data" / "etichette_oro.jsonl")
    prev = [dict(o, assegnazione_automatica=True) for o in oro]
    rapporto = valuta(prev, oro)
    assert rapporto["tutti_i_campi_corretti"] == 1.0
