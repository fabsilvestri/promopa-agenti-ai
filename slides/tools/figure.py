import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import json, textwrap
from pathlib import Path

OUT = Path("slides/tools/fig"); OUT.mkdir(exist_ok=True)
BORD = "#822433"; BLU = "#1B3A5F"; AZZ = "#E9F1F8"; GRIG = "#595959"; NERO = "#212121"; VERDE = "#2C6E49"; ARANC = "#C8772B"
plt.rcParams["font.family"] = "DejaVu Sans"


def box(ax, x, y, w, h, testo, fc=AZZ, ec=BLU, fs=11, tc=NERO, bold=False, lw=1.5, r=0.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, testo, ha="center", va="center", fontsize=fs, color=tc,
            fontweight="bold" if bold else "normal", linespacing=1.3)


def arrow(ax, x1, y1, x2, y2, color=GRIG):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16, color=color, lw=1.6))


def fresh(w=10, h=5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=200)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


def salva(fig, nome):
    fig.savefig(OUT / nome, bbox_inches="tight", pad_inches=0.05, transparent=False, facecolor="white")
    plt.close(fig)


def tabella(ax, colonne, righe, evidenzia=None, fs=11, altezza=2.0, allinea="left"):
    """Tabella con uno stile piu' quieto di quello di default di matplotlib.

    Niente righe verticali, separatori orizzontali chiarissimi, intestazione
    piena in blu, righe alternate appena tinte. `evidenzia` e' una funzione
    (indice_riga, indice_colonna, valore) -> colore di sfondo, oppure None.
    """
    t = ax.table(cellText=righe, colLabels=colonne, loc="center",
                 cellLoc=allinea, colLoc=allinea)
    t.auto_set_font_size(False); t.set_fontsize(fs); t.scale(1, altezza)
    for (i, j), c in t.get_celld().items():
        c.set_linewidth(0.8)
        c.visible_edges = "horizontal"
        c.set_edgecolor("#E4E7EB")
        c.PAD = 0.055
        if i == 0:
            c.set_facecolor(BLU); c.set_edgecolor(BLU)
            c.visible_edges = "closed"
            c.set_text_props(color="white", fontweight="bold")
        else:
            c.set_facecolor("#FFFFFF" if i % 2 else "#F7F9FB")
            colore = evidenzia(i - 1, j, righe[i - 1][j]) if evidenzia else None
            if colore:
                c.set_facecolor(colore)
    t.auto_set_column_width(col=list(range(len(colonne))))
    return t


# 1. chatbot / workflow / agente
fig, ax = fresh(10, 4.6)
cols = [("Chatbot", "Risponde a una domanda.\nNessuna azione,\nnessun passo successivo.", AZZ),
        ("Workflow", "Passi decisi da noi.\nL'AI dentro uno o più passi.\nPrevedibile, misurabile.", "#DCE8DC"),
        ("Agente", "Decide lui i passi\ne quando fermarsi.\nFlessibile, meno prevedibile.", "#F6E7D8")]
for i, (t, d, c) in enumerate(cols):
    x = 0.03 + i * 0.325
    box(ax, x, 0.55, 0.29, 0.28, t, fc=c, fs=16, bold=True, tc=BLU)
    ax.text(x + 0.145, 0.42, d, ha="center", va="top", fontsize=11.5, color=NERO, linespacing=1.4)
ax.annotate("", xy=(0.97, 0.06), xytext=(0.03, 0.06), arrowprops=dict(arrowstyle="-|>", color=GRIG, lw=1.5))
ax.text(0.5, 0.0, "autonomia crescente, controllo decrescente", ha="center", va="bottom", fontsize=10, color=GRIG, style="italic")
salva(fig, "chatbot_workflow_agente.png")

# 2. anatomia
fig, ax = fresh(8, 5.2)
box(ax, 0.33, 0.40, 0.34, 0.20, "Modello\n(ragiona sul testo)", fc="#F6E7D8", fs=13, bold=True)
pezzi = [(0.03, 0.72, "Strumenti\ne-mail, Zoom, Moodle, sito"), (0.59, 0.72, "Memoria\ntassonomia, storico"),
         (0.03, 0.08, "Ciclo di azione\nleggi, decidi, agisci, verifica"), (0.59, 0.08, "Controllo umano\nsoglia, coda, invio")]
for x, y, t in pezzi:
    fc = "#DCE8DC" if "umano" in t else AZZ
    box(ax, x, y, 0.38, 0.20, t, fc=fc, fs=11)
for (x, y, _) in pezzi:
    cx, cy = x + 0.19, y + 0.10
    tx, ty = 0.5, 0.5
    dx, dy = tx - cx, ty - cy
    arrow(ax, cx + dx * 0.35, cy + dy * 0.35, tx - dx * 0.42, ty - dy * 0.42)
salva(fig, "anatomia_agente.png")

# 3. pattern
fig, ax = fresh(10, 4.6)
box(ax, 0.02, 0.62, 0.20, 0.20, "Richiesta", fs=12, bold=True)
box(ax, 0.30, 0.62, 0.22, 0.20, "Routing\n(classifica)", fc="#F6E7D8", fs=12)
for j, t in enumerate(["Segreteria", "Amministrazione", "Tutor", "Coda umana"]):
    y = 0.92 - j * 0.16
    fc = "#DCE8DC" if "umana" in t else AZZ
    box(ax, 0.66, y - 0.055, 0.30, 0.11, t, fc=fc, fs=11)
    arrow(ax, 0.52, 0.72, 0.66, y)
arrow(ax, 0.22, 0.72, 0.30, 0.72)
ax.text(0.02, 0.50, "Routing: una richiesta, un destinatario.\nSotto soglia: coda umana.", fontsize=11, color=NERO, va="top")
box(ax, 0.02, 0.02, 0.20, 0.20, "Chat Zoom\n17 righe", fs=11, bold=True)
box(ax, 0.30, 0.02, 0.22, 0.20, "Estrazione\nstrutturata", fc="#F6E7D8", fs=12)
box(ax, 0.66, 0.02, 0.30, 0.20, "4 richieste\ncon campi fissi", fs=11)
arrow(ax, 0.22, 0.12, 0.30, 0.12); arrow(ax, 0.52, 0.12, 0.66, 0.12)
salva(fig, "pattern.png")

# 4. mappa esigenze
fig, ax = plt.subplots(figsize=(11, 3.4), dpi=200); ax.axis("off")
cols = ["Esigenza", "Natura", "Cosa serve davvero"]
cells = [["1. Repository unico", "Integrazione", "Connettori da 5 caselle e moduli verso un contenitore unico"],
         ["2. Zoom e Moodle", "AI", "Estrarre richieste da testo non strutturato"],
         ["3. Classificazione", "AI + regola", "Il modello applica la tassonomia, la soglia decide"],
         ["4. Tracciamento", "Workflow + AI", "Stati e scadenze deterministici, bozze, invio umano"]]
tinte = {"Integrazione": "#D3E5D6", "AI": "#F7DFC4", "AI + regola": "#F7DFC4", "Workflow + AI": "#D3E5D6"}
tabella(ax, cols, cells, fs=11.5, altezza=2.2,
        evidenzia=lambda i, j, v: tinte.get(v) if j == 1 else None)
salva(fig, "mappa_esigenze.png")

# 5. pipeline
fig, ax = fresh(11, 4.2)
passi = [("Fonti\n5 caselle,\nmoduli, Moodle", AZZ), ("Repository\nunico", "#DCE8DC"), ("Estrazione\n(Zoom,\nquestionari)", "#F6E7D8"),
         ("Classifica\n+ confidenza", "#F6E7D8"), ("Coda per\noperatore", "#DCE8DC"), ("Bozza di\nrisposta", "#F6E7D8"), ("Invio e\nchiusura", "#DCE8DC")]
n = len(passi); w = 0.128; gap = (1 - n * w) / (n - 1)
for i, (t, fc) in enumerate(passi):
    x = i * (w + gap)
    box(ax, x, 0.45, w, 0.34, t, fc=fc, fs=9.5, bold=(fc == "#F6E7D8"))
    if i < n - 1:
        arrow(ax, x + w, 0.60, x + w + gap, 0.60)
ax.text(0.064, 0.32, "integrazione", ha="center", fontsize=10, color=VERDE)
ax.text(0.5, 0.32, "AI = arancio", ha="center", fontsize=10, color=ARANC)
ax.text(1 - 0.064, 0.32, "umano", ha="center", fontsize=10, color=VERDE)
box(ax, 0.30, 0.03, 0.40, 0.17, "Sotto soglia di confidenza: salta l'assegnazione,\nla richiesta va a un umano", fc="white", ec=GRIG, fs=10)
arrow(ax, 0.50, 0.45, 0.50, 0.21, color=GRIG)
salva(fig, "pipeline.png")

# 6. tabella demo
_tutte = [json.loads(r) for r in open("demo/output_esempio/richieste_classificate.jsonl", encoding="utf-8")]
# Sulla slide ci stanno dieci righe: si scelgono per coprire tutti i canali,
# tenendo dentro le urgenze alte e qualche esempio reale della Fondazione.
_scelti = ["R001", "R003", "R004", "R007", "RE01", "RE05", "RE10", "Z-1048", "Q03", "Q06"]
_per_id = {r["id"]: r for r in _tutte}
righe = [_per_id[i] for i in _scelti if i in _per_id] or _tutte[:10]
fig, ax = plt.subplots(figsize=(11, 4.4), dpi=200); ax.axis("off")
cols = ["id", "canale", "corso", "tipologia", "urgenza", "operatore", "conf."]
cells = [[r["id"], r["canale"], r["corso"], r["tipologia"], r["urgenza"],
          r["operatore"] if r["assegnazione_automatica"] else "DA VERIFICARE", f"{r['confidenza']:.2f}"] for r in righe]
def _tinta(i, j, v):
    if cells[i][5] == "DA VERIFICARE":
        return "#F8D7D2"
    if cells[i][4] == "alta":
        return "#FBE3C2"
    return None


tabella(ax, cols, cells, fs=10.5, altezza=1.9, evidenzia=_tinta)
salva(fig, "tabella_demo.png")

# 7. quattro passi
fig, ax = fresh(11, 3.6)
passi = [("1. Audit", "canali, volumi,\ntempi (1-2 sett.)"), ("2. Tassonomia\ne dati", "100-200 richieste\netichettate (2 sett.)"),
         ("3. Prototipo", "contenitore, connettori,\nclassificatore (2-4 sett.)"), ("4. Misura\ne decidi", "un mese di metriche,\npoi estendere o fermare")]
for i, (t, d) in enumerate(passi):
    x = 0.02 + i * 0.245
    box(ax, x, 0.50, 0.21, 0.30, t, fc=AZZ if i % 2 == 0 else "#DCE8DC", fs=13, bold=True, tc=BLU)
    ax.text(x + 0.105, 0.42, d, ha="center", va="top", fontsize=10.5, color=NERO, linespacing=1.3)
    if i < 3:
        arrow(ax, x + 0.21, 0.65, x + 0.245, 0.65)
salva(fig, "quattro_passi.png")

# 8. griglia esempio
fig, ax = plt.subplots(figsize=(11, 4.4), dpi=200); ax.axis("off")
cols = ["#", "Passo", "Input", "Decisione", "Tipo"]
cells = [["1", "Raccogliere le richieste", "5 caselle, moduli, Moodle", "nessuna", "Integrazione"],
         ["2", "Estrarre da Zoom e questionari", "chat, risposte aperte", "è una richiesta?", "AI"],
         ["3", "Classificare corso, tipo, urgenza", "testo richiesta", "tassonomia", "AI"],
         ["4", "Assegnare operatore", "tipologia", "competenze per ruolo", "Regola"],
         ["5", "Verificare bassa confidenza", "coda 'da verificare'", "giudizio", "Umano"],
         ["6", "Scrivere la risposta", "richiesta + contesto", "cosa rispondere", "AI"],
         ["7", "Inviare e chiudere", "bozza", "approvazione", "Umano"]]
colori = {"AI": "#F7DFC4", "Umano": "#D3E5D6", "Integrazione": "#DCE7F2", "Regola": "#DCE7F2"}
tabella(ax, cols, cells, fs=11, altezza=1.9,
        evidenzia=lambda i, j, v: colori.get(v) if j == 4 else None)
salva(fig, "griglia.png")

# 9. numeri: nessuna figura, si fanno con shape in pptx
print("ok")


# =====================================================================
# Figure aggiunte: scaletta, ciclo, canali, stati, griglia vuota,
# ruoli, calendario, e i tre grafici sui numeri veri della pipeline.
# =====================================================================
# Coppia di colori per i grafici a due categorie: passa i controlli sul
# daltonismo (deutan e protan sopra deltaE 15), a differenza di bordeaux
# contro verde che e' la coppia sbagliata piu' comune nei deck.
# Coppia validata per i grafici a due categorie. Nome diverso da BLU per non
# coprirlo: BLU e' il blu dei titoli e dei diagrammi, questo e' il blu dei dati.
ROSSO_DATI = "#A82F44"
BLU_DATI = "#2E6E9E"
VALUTAZIONE = json.loads(Path("demo/output_esempio/valutazione.json").read_text(encoding="utf-8"))


# 10. scaletta della giornata
fig, ax = fresh(11, 3.2)
blocchi = [("1\nRiaggancio", "10'"), ("2\nAnatomia", "20'"), ("3\nIl caso", "30'"),
           ("4\nLimiti", "15'"), ("5\nPilota", "15'"), ("6\nEsercitazione", "30'")]
n = len(blocchi); gap = 0.012; w = (1 - gap * (n - 1)) / n
for i, (t, m) in enumerate(blocchi):
    x = i * (w + gap)
    box(ax, x, 0.42, w, 0.40, t, fc=AZZ if i % 2 == 0 else "#DCE8DC", fs=12, bold=True, tc=BLU)
    ax.text(x + w / 2, 0.33, m, ha="center", va="top", fontsize=13, color=GRIG)
ax.annotate("", xy=(1.0, 0.13), xytext=(0.0, 0.13), arrowprops=dict(arrowstyle="-|>", color=GRIG, lw=1.4))
ax.text(0.5, 0.03, "due ore, con una pausa dentro il blocco 3", ha="center", fontsize=10.5, color=GRIG, style="italic")
salva(fig, "scaletta.png")

# 11. ciclo di azione
fig, ax = fresh(8, 4.2)
passi = [("Leggi", 0.50, 0.80), ("Decidi", 0.82, 0.50), ("Agisci", 0.50, 0.20), ("Verifica", 0.18, 0.50)]
for t, cx, cy in passi:
    box(ax, cx - 0.15, cy - 0.09, 0.30, 0.18, t, fc=AZZ, fs=14, bold=True, tc=BLU)
for i in range(4):
    _, x1, y1 = passi[i]
    _, x2, y2 = passi[(i + 1) % 4]
    dx, dy = x2 - x1, y2 - y1
    arrow(ax, x1 + dx * 0.30, y1 + dy * 0.30, x2 - dx * 0.30, y2 - dy * 0.30)
ax.text(0.50, 0.50, "e poi\nda capo", ha="center", va="center", fontsize=12, color=GRIG, style="italic")
salva(fig, "ciclo_azione.png")

# 12. i canali in ingresso
fig, ax = fresh(11, 4.0)
fonti = [("5 caselle\ne-mail", AZZ), ("Moduli\ndel sito", AZZ), ("Messaggi\nMoodle", AZZ),
         ("Questionari\nMoodle", "#F6E7D8"), ("Chat\nZoom", "#F6E7D8")]
n = len(fonti); gap = 0.03; w = (1 - gap * (n - 1)) / n
for i, (t, fc) in enumerate(fonti):
    x = i * (w + gap)
    box(ax, x, 0.68, w, 0.24, t, fc=fc, fs=12)
    arrow(ax, x + w / 2, 0.66, 0.44, 0.50)
box(ax, 0.33, 0.26, 0.22, 0.22, "Contenitore\nunico", fc="#DCE8DC", fs=14, bold=True)
arrow(ax, 0.56, 0.37, 0.66, 0.37)
box(ax, 0.67, 0.26, 0.22, 0.22, "Coda per\noperatore", fc=AZZ, fs=13)
ax.text(0.5, 0.08, "azzurro: oggi arriva a qualcuno   ·   arancio: oggi si perde",
        ha="center", fontsize=12, color=GRIG, style="italic")
salva(fig, "canali.png")

# 13. stati di una richiesta
fig, ax = fresh(11, 2.8)
stati = ["nuova", "presa in carico", "in attesa utente", "chiusa"]
n = len(stati); gap = 0.05; w = (1 - gap * (n - 1)) / n
for i, t in enumerate(stati):
    x = i * (w + gap)
    box(ax, x, 0.45, w, 0.32, t, fc=AZZ, fs=13, bold=True, tc=BLU)
    if i < n - 1:
        arrow(ax, x + w, 0.61, x + w + gap, 0.61)
# il ritorno da "in attesa utente" a "presa in carico", disegnato sotto i box
ax.annotate("", xy=(0.36, 0.43), xytext=(0.64, 0.43),
            arrowprops=dict(arrowstyle="-|>", color=GRIG, lw=1.4, connectionstyle="arc3,rad=0.45"))
ax.text(0.5, 0.10, "nessuna AI: sono regole e date", ha="center", fontsize=12, color=VERDE)
salva(fig, "stati.png")

# 14. griglia vuota da compilare
fig, ax = plt.subplots(figsize=(11, 3.8), dpi=200); ax.axis("off")
cols = ["#", "Passo", "Chi lo fa oggi", "Input", "Decisione", "Output", "Tipo"]
cells = [[str(i), "", "", "", "", "", ""] for i in range(1, 7)]
tabella(ax, cols, cells, fs=11.5, altezza=2.4)
salva(fig, "griglia_vuota.png")

# 15. chi fa cosa nel pilota
fig, ax = plt.subplots(figsize=(11, 3.4), dpi=200); ax.axis("off")
cols = ["Passo", "Chi lo guida", "Chi partecipa", "Quanto tempo"]
cells = [["1. Audit", "Segreteria", "Chi risponde oggi", "1-2 settimane"],
         ["2. Tassonomia e dati", "Segreteria", "Due persone che etichettano", "2 settimane"],
         ["3. Prototipo", "Chi sa usare lo strumento", "Segreteria", "2-4 settimane"],
         ["4. Misura e decidi", "Direzione", "Tutti", "1 mese"]]
tabella(ax, cols, cells, fs=11.5, altezza=2.2,
        evidenzia=lambda i, j, v: "#DCE7F2" if j == 0 else None)
salva(fig, "ruoli.png")

# 16. calendario del pilota
fig, ax = fresh(11, 3.0)
barre = [("1. Audit", 0.00, 0.18, AZZ), ("2. Tassonomia e dati", 0.18, 0.22, "#DCE8DC"),
         ("3. Prototipo", 0.40, 0.30, "#F6E7D8"), ("4. Misura", 0.70, 0.28, AZZ)]
for i, (t, x, w, fc) in enumerate(barre):
    y = 0.72 - i * 0.17
    box(ax, x, y, w, 0.13, t, fc=fc, fs=10.5, r=0.01)
for k, etichetta in enumerate(["oggi", "+1 mese", "+2 mesi", "+3 mesi"]):
    ax.text(k / 3.2, 0.05, etichetta, ha="center", fontsize=10, color=GRIG)
    ax.plot([k / 3.2, k / 3.2], [0.10, 0.92], color="#DDDDDD", lw=1, zorder=0)
salva(fig, "calendario.png")

# 17. accuratezza per campo, numeri veri
fig, ax = plt.subplots(figsize=(9, 3.6), dpi=200)
acc = VALUTAZIONE["accuratezza"]
voci = [("corso", acc["corso"]), ("tipologia", acc["tipologia"]),
        ("operatore", acc["operatore"]), ("urgenza", acc["urgenza"]),
        ("tutti e quattro", VALUTAZIONE["tutti_i_campi_corretti"])]
voci.sort(key=lambda v: v[1])
y = range(len(voci))
ax.barh(list(y), [v * 100 for _, v in voci], height=0.55, color=BLU_DATI, zorder=3)
ax.axvline(80, color=GRIG, lw=1.4, ls="--", zorder=4)
ax.text(80.8, len(voci) - 0.35, "soglia 80%", fontsize=10, color=GRIG)
for i, (nome, v) in enumerate(voci):
    etichetta = f"{v * 100:.0f}%" if abs(v * 100 - round(v * 100)) < 0.05 else f"{v * 100:.1f}%".replace(".", ",")
    ax.text(v * 100 - 1.5, i, etichetta, va="center", ha="right",
            fontsize=12, color="white", fontweight="bold", zorder=5)
ax.set_yticks(list(y)); ax.set_yticklabels([n for n, _ in voci], fontsize=12)
ax.set_xlim(0, 105); ax.set_xlabel("richieste classificate correttamente", fontsize=10.5, color=GRIG)
ax.xaxis.set_major_formatter(lambda v, p: f"{v:.0f}%")
for lato in ("top", "right", "left"):
    ax.spines[lato].set_visible(False)
ax.spines["bottom"].set_color("#CCCCCC")
ax.tick_params(colors=GRIG, length=0)
ax.grid(axis="x", color="#EEEEEE", zorder=0)
ax.set_axisbelow(True)
fig.tight_layout()
salva(fig, "accuratezza.png")

# 18. confidenza dichiarata contro correttezza: il grafico che fa il punto
fig, ax = plt.subplots(figsize=(10, 3.4), dpi=200)
per_r = VALUTAZIONE["per_richiesta"]
giuste = [r["confidenza"] for r in per_r if not r["campi_sbagliati"]]
storte = [r["confidenza"] for r in per_r if r["campi_sbagliati"]]
import random
random.seed(7)
ax.scatter(giuste, [1 + random.uniform(-0.13, 0.13) for _ in giuste], s=110,
           color=BLU_DATI, alpha=0.85, edgecolor="white", linewidth=1.2, zorder=3,
           label=f"tutti i campi corretti ({len(giuste)})")
ax.scatter(storte, [0 + random.uniform(-0.13, 0.13) for _ in storte], s=110,
           color=ROSSO_DATI, alpha=0.85, edgecolor="white", linewidth=1.2, zorder=3,
           marker="X", label=f"almeno un campo sbagliato ({len(storte)})")
ax.axvline(0.7, color=NERO, lw=1.8, zorder=4)
ax.text(0.697, 1.42, "soglia 0,7: sotto qui\nla richiesta va a un umano",
        ha="right", va="top", fontsize=10.5, color=NERO)
ax.set_xlim(0.55, 1.0); ax.set_ylim(-0.5, 1.5)
ax.set_yticks([0, 1]); ax.set_yticklabels(["sbagliate", "corrette"], fontsize=12)
ax.set_xlabel("confidenza dichiarata dal modello", fontsize=10.5, color=GRIG)
for lato in ("top", "right", "left"):
    ax.spines[lato].set_visible(False)
ax.spines["bottom"].set_color("#CCCCCC")
ax.tick_params(colors=GRIG, length=0)
ax.grid(axis="x", color="#EEEEEE", zorder=0); ax.set_axisbelow(True)
ax.legend(loc="center left", frameon=False, fontsize=10.5)
fig.tight_layout()
salva(fig, "confidenza.png")

# 19. dove si concentrano gli errori
fig, ax = plt.subplots(figsize=(9, 3.2), dpi=200)
errori = VALUTAZIONE["errori"]
ordine = ["urgenza", "tipologia", "operatore", "corso"]
conteggi = [len(errori.get(c, [])) for c in ordine]
ax.bar(ordine, conteggi, width=0.5, color=BLU_DATI, zorder=3)
for i, c in enumerate(conteggi):
    ax.text(i, c + 0.25, str(c), ha="center", fontsize=13, color=NERO, fontweight="bold")
ax.set_ylim(0, max(conteggi) + 2)
ax.set_ylabel("richieste sbagliate su 40", fontsize=10.5, color=GRIG)
for lato in ("top", "right"):
    ax.spines[lato].set_visible(False)
ax.spines["left"].set_color("#CCCCCC"); ax.spines["bottom"].set_color("#CCCCCC")
ax.tick_params(colors=GRIG, length=0, labelsize=12)
ax.grid(axis="y", color="#EEEEEE", zorder=0); ax.set_axisbelow(True)
fig.tight_layout()
salva(fig, "errori_campi.png")
