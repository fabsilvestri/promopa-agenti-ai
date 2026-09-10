"""Genera le fotografie del deck con gpt-image-1.

Non sono diagrammi: i diagrammi restano in figure.py e portano informazione.
Queste sono immagini di copertina, di sezione e di respiro.

Tre regole nei prompt, che sono anche i tre punti dove il fotorealismo si
rompe: niente volti riconoscibili, niente testo leggibile, niente marchi.
In più: niente che assomigli a una sede o a persone reali della Fondazione,
perché una foto inventata di un'organizzazione vera inganna chi la guarda.

Uso:
    export OPENAI_API_KEY=...
    python slides/tools/foto.py            # genera solo quelle che mancano
    python slides/tools/foto.py --tutte    # rigenera tutto
"""
from __future__ import annotations

import argparse
import base64
import io
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from openai import OpenAI
from PIL import Image

USCITA = Path("slides/tools/fig/foto")
MODELLO = "gpt-image-1"
DIMENSIONE = "1536x1024"
QUALITA = "high"

COMUNE = (
    "Fotografia realistica, scattata con reflex a pieno formato, obiettivo 35mm, "
    "profondità di campo naturale, luce ambientale credibile, colori sobri, "
    "nessun filtro vistoso, nessun effetto HDR. "
    "Nessun volto riconoscibile, nessuna persona in primo piano. "
    "Nessun testo leggibile, nessuna scritta, nessun logo, nessun marchio. "
    "Composizione orizzontale, ampia, con spazio libero nella parte alta."
)

FOTO: dict[str, str] = {
    # --- copertina e sezioni -------------------------------------------------
    "copertina": (
        "Il corridoio di un edificio pubblico italiano di primo Novecento, "
        "pavimento in graniglia, alte finestre a sinistra, luce del primo "
        "mattino che taglia il pavimento in diagonale, nessuno in giro."
    ),
    "sez1_riaggancio": (
        "Un'aula di formazione vuota vista dall'ultima fila, sedie in legno e "
        "metallo allineate, uno schermo spento in fondo, luce calda da una "
        "finestra laterale, pulviscolo nell'aria."
    ),
    "sez2_anatomia": (
        "Vista dall'alto di un banco da lavoro con i pezzi smontati di un "
        "orologio meccanico da tavolo, ottone e acciaio, disposti ordinatamente "
        "su un panno grigio, pinzette accanto, luce radente da sinistra."
    ),
    "sez3_helpdesk": (
        "Una scrivania di segreteria vista di tre quarti, una vaschetta "
        "portadocumenti di metallo colma di fogli, una cuffia con microfono "
        "appoggiata di lato, un telefono fisso, luce di ufficio a fine giornata."
    ),
    "sez4_limiti": (
        "Primo piano di un moschettone d'acciaio e di una corda da arrampicata "
        "arancione fissati a un ancoraggio nella roccia grigia, luce di alta "
        "montagna, sfondo sfocato di valle."
    ),
    "sez5_pilota": (
        "Il plastico in cartoncino di un edificio su un tavolo da architetto, "
        "accanto rotoli di disegni e una squadra, luce calda da lampada da "
        "tavolo, fondo scuro."
    ),
    "sez6_esercitazione": (
        "Vista dall'alto di un tavolo di legno chiaro con quattro paia di mani "
        "che lavorano su fogli quadrettati, matite, un evidenziatore, tazzine "
        "di caffè ai bordi. Solo mani e avambracci, nessun volto."
    ),
    "sez7_grazie": (
        "L'interno di una sala storica italiana con volte alte e finestroni, "
        "la luce del tardo pomeriggio che entra di traverso e disegna rettangoli "
        "sul pavimento di cotto, la sala è vuota."
    ),
    # --- slide di contenuto --------------------------------------------------
    "c03_da_giugno": (
        "Una scrivania di legno accanto a una finestra con persiane socchiuse, "
        "un portatile chiuso, una tazzina di caffè vuota, luce di settembre a "
        "strisce sul piano."
    ),
    "c05_tesi": (
        "Macro di una penna stilografica appoggiata su un taccuino aperto a "
        "pagine bianche rigate, carta spessa, luce morbida laterale, "
        "sfondo di legno scuro sfocato."
    ),
    "c11_regola": (
        "Primo piano di un vecchio interruttore della luce in ceramica bianca "
        "su un muro intonacato color sabbia, ombra netta, luce naturale radente."
    ),
    "c15_repository": (
        "Una parete di cassette postali in ottone di un vecchio ufficio postale, "
        "sportelli tutti uguali, alcuni socchiusi, luce calda che scende "
        "dall'alto, prospettiva leggermente laterale."
    ),
    "c21_demo": (
        "Un portatile aperto su un leggio di legno visto da dietro, la luce "
        "dello schermo che illumina il leggio, in fondo la sagoma sfocata di "
        "una sala con sedie, nessun volto distinguibile."
    ),
    "c36_consegna": (
        "Vista dall'alto di un foglio a griglia vuoto su un tavolo, accanto due "
        "matite temperate e una gomma, luce diffusa da studio."
    ),
    "c38_restituzione": (
        "Un cavalletto con un blocco di fogli grandi bianchi in una sala "
        "riunioni luminosa, pennarelli sul bordo, i fogli sono vuoti, "
        "nessuna persona."
    ),
    "c39_errori": (
        "Vista dall'alto di tre palle di carta accartocciata su un pavimento di "
        "legno accanto a un cestino di metallo forato, luce laterale che "
        "allunga le ombre."
    ),
    # --- seconda serie, per le slide aggiunte --------------------------------
    "ap_portate": (
        "Una borsa di cuoio consumato e un quaderno chiuso su una panca di legno "
        "in un atrio, luce del mattino da una vetrata alle spalle."
    ),
    "an_modello": (
        "Una scacchiera di legno a metà partita vista di lato, pezzi in "
        "boxwood ed ebano, profondità di campo cortissima, fondo scuro."
    ),
    "an_strumenti": (
        "Un pannello portautensili da officina visto di fronte, chiavi e pinze "
        "appese in ordine di misura, ombre nette, parete di legno chiaro."
    ),
    "an_memoria": (
        "Uno schedario da biblioteca in legno con un cassetto aperto e le schede "
        "di cartoncino in fila, luce calda laterale, sfondo sfocato."
    ),
    "an_controllo": (
        "Le leve di ottone e acciaio di una cabina di manovra ferroviaria "
        "d'epoca, allineate in fila, luce che entra da una finestra laterale."
    ),
    "an_fornitore": (
        "Due sedie vuote una di fronte all'altra ai capi di un tavolo lungo in "
        "una sala riunioni luminosa, nessuno seduto, tende chiare."
    ),
    "hd_canali": (
        "Primo piano dei cavi con spinotti di un vecchio centralino telefonico "
        "a innesto, ottone ossidato e tessuto colorato, luce morbida."
    ),
    "hd_ruoli": (
        "Cinque sedie da ufficio identiche allineate lungo una parete chiara "
        "vuota, vista laterale, pavimento in linoleum, luce diffusa."
    ),
    "hd_dodici": (
        "Una pila ordinata di buste da lettera bianche chiuse su una scrivania "
        "di legno scuro, luce radente da sinistra, nessuna scritta."
    ),
    "li_storto": (
        "Una fila di tessere del domino nere cadute una sull'altra su un tavolo "
        "di legno scuro, luce laterale bassa, ombre lunghe."
    ),
    "li_costi": (
        "Un vecchio pallottoliere di legno con palline colorate, primo piano di "
        "tre quarti, luce calda da una finestra, fondo neutro."
    ),
    "pi_scritto": (
        "Una penna stilografica appoggiata su un documento appena firmato, "
        "macro, la firma è una macchia di inchiostro non leggibile, carta spessa."
    ),
    "pi_fermarsi": (
        "Un paraurti di fine binario in una stazione ferroviaria di provincia, "
        "rotaie e ghiaia, luce del primo mattino, nessuno sul marciapiede."
    ),
    "es_processi": (
        "Tre cartelline di cartone di colori diversi impilate leggermente "
        "sfalsate su una scrivania chiara, vista dall'alto, luce da studio."
    ),
    # --- terza serie: le immagini che devono far sorridere -------------------
    # Comiche per accumulo, non per caricatura: nessuno viene preso in giro,
    # e restano fotografie plausibili di uffici che esistono davvero.
    "gag_faldoni": (
        "Una torre di faldoni di cartone impilati fino a sfiorare il soffitto in "
        "un ufficio, leggermente inclinata, accanto a una scrivania minuscola e "
        "ordinata, luce al neon."
    ),
    "gag_postit": (
        "Un monitor da ufficio completamente ricoperto di foglietti adesivi "
        "gialli sui bordi e sullo schermo, decine di foglietti sovrapposti, "
        "i foglietti sono vuoti, luce di ufficio."
    ),
    "gag_telefoni": (
        "Cinque telefoni fissi di modelli ed epoche diverse allineati sulla "
        "stessa scrivania, i cavi aggrovigliati fra loro, vista di tre quarti."
    ),
    "gag_robot": (
        "Un robot giocattolo di latta anni Cinquanta seduto su una sedia "
        "girevole da ufficio davanti a una tastiera, altezza degli occhi del "
        "robot ben sotto il piano della scrivania, ufficio vuoto sullo sfondo."
    ),
    "gag_pulsante": (
        "Un grande pulsante rosso da fabbrica sotto una teca di vetro, "
        "appoggiato su una scrivania d'ufficio in mezzo a fogli e graffette, "
        "luce laterale, nessuna scritta sulla teca."
    ),
    "gag_cavi": (
        "Un groviglio enorme di cavi di rete colorati che esce da un armadio "
        "tecnico aperto e ricade a terra, primo piano, luce fredda."
    ),
    "gag_stampante": (
        "Una vecchia stampante ad aghi su un carrello che ha srotolato a terra "
        "un nastro di carta continua lunghissimo, la carta si accumula sul "
        "pavimento in pieghe, corridoio di ufficio."
    ),
    "gag_cane": (
        "Un cane di taglia media che dorme raggomitolato sotto una scrivania "
        "da ufficio, accanto ai piedi di una sedia girevole, luce calda, "
        "nessuna persona inquadrata."
    ),
    "gag_pianta": (
        "Una pianta da appartamento completamente secca in un vaso di "
        "terracotta accanto a una scrivania impeccabilmente ordinata, "
        "contrasto evidente, luce da finestra."
    ),
    "gag_ombrello": (
        "Un ombrello nero aperto appoggiato a terra in un corridoio di ufficio, "
        "sotto una macchia di umidità sul soffitto, secchio di plastica accanto."
    ),
    "gag_carrello": (
        "Un carrello portadocumenti di metallo stracarico di faldoni in un "
        "corridoio, alcuni fogli scivolati a terra dietro di lui, "
        "movimento leggermente mosso."
    ),
    "gag_timbri": (
        "Una decina di timbri di gomma appesi a un supporto girevole da "
        "scrivania, primo piano, le impronte dei timbri non sono leggibili, "
        "luce radente."
    ),
    "hd_coda": (
        "Una fila di sedie di plastica vuote lungo il muro di un corridoio di "
        "ufficio pubblico, luce al neon, pavimento lucido."
    ),
    "pi_metro": (
        "Un metro a nastro d'acciaio srotolato su un tavolo di legno chiaro, "
        "le tacche non sono leggibili, luce laterale netta, fondo pulito."
    ),
}


def genera(cliente: OpenAI, nome: str, soggetto: str) -> str:
    risposta = cliente.images.generate(
        model=MODELLO, prompt=f"{soggetto} {COMUNE}",
        size=DIMENSIONE, quality=QUALITA, n=1,
    )
    grezza = base64.b64decode(risposta.data[0].b64_json)
    # Il PNG a piena qualità pesa oltre un mega: nel deck non serve.
    immagine = Image.open(io.BytesIO(grezza)).convert("RGB")
    destinazione = USCITA / f"{nome}.jpg"
    immagine.save(destinazione, "JPEG", quality=88, optimize=True)
    return f"{nome}: {destinazione.stat().st_size // 1024} KB"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tutte", action="store_true", help="rigenera anche quelle già presenti")
    ap.add_argument("--solo", nargs="*", help="genera solo questi nomi")
    args = ap.parse_args()

    USCITA.mkdir(parents=True, exist_ok=True)
    cliente = OpenAI()
    da_fare = {
        n: s for n, s in FOTO.items()
        if (not args.solo or n in args.solo) and (args.tutte or not (USCITA / f"{n}.jpg").exists())
    }
    if not da_fare:
        print("Niente da generare.")
        return
    print(f"Genero {len(da_fare)} immagini con {MODELLO} ({QUALITA}, {DIMENSIONE})...")
    with ThreadPoolExecutor(max_workers=4) as pool:
        futuri = {pool.submit(genera, cliente, n, s): n for n, s in da_fare.items()}
        for f in futuri:
            try:
                print("  ", f.result())
            except Exception as errore:  # una foto che salta non deve fermare le altre
                print(f"   ERRORE su {futuri[f]}: {type(errore).__name__}: {errore}", file=sys.stderr)


if __name__ == "__main__":
    main()
