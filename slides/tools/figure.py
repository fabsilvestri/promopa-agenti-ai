import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import json, textwrap
from pathlib import Path

OUT = Path("slides/tools/fig"); OUT.mkdir(exist_ok=True)
BORD = "#822433"; AZZ = "#E9F1F8"; GRIG = "#595959"; NERO = "#212121"; VERDE = "#2C6E49"; ARANC = "#C8772B"
plt.rcParams["font.family"] = "DejaVu Sans"


def box(ax, x, y, w, h, testo, fc=AZZ, ec=BORD, fs=11, tc=NERO, bold=False, lw=1.5, r=0.02):
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


# 1. chatbot / workflow / agente
fig, ax = fresh(10, 4.6)
cols = [("Chatbot", "Risponde a una domanda.\nNessuna azione,\nnessun passo successivo.", AZZ),
        ("Workflow", "Passi decisi da noi.\nL'AI dentro uno o più passi.\nPrevedibile, misurabile.", "#DCE8DC"),
        ("Agente", "Decide lui i passi\ne quando fermarsi.\nFlessibile, meno prevedibile.", "#F6E7D8")]
for i, (t, d, c) in enumerate(cols):
    x = 0.03 + i * 0.325
    box(ax, x, 0.55, 0.29, 0.28, t, fc=c, fs=16, bold=True, tc=BORD)
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
fig, ax = fresh(10, 4.8)
righe = [("1. Repository unico", "Integrazione", "Connettori da 5 caselle e moduli\nverso un contenitore unico", "#DCE8DC"),
         ("2. Zoom e Moodle", "AI", "Estrarre richieste da testo\nnon strutturato", "#F6E7D8"),
         ("3. Classificazione", "AI + regola", "Modello applica la tassonomia;\nsoglia di confidenza", "#F6E7D8"),
         ("4. Tracciamento", "Workflow + AI", "Stati e scadenze deterministici;\nbozze generate, invio umano", "#DCE8DC")]
ax.text(0.03, 0.96, "Esigenza", fontsize=12, fontweight="bold", color=BORD, va="top")
ax.text(0.40, 0.96, "Natura", fontsize=12, fontweight="bold", color=BORD, va="top")
ax.text(0.60, 0.96, "Cosa serve davvero", fontsize=12, fontweight="bold", color=BORD, va="top")
for i, (e, n, c, fc) in enumerate(righe):
    y = 0.72 - i * 0.22
    box(ax, 0.02, y, 0.34, 0.17, e, fc=AZZ, fs=12, bold=True)
    box(ax, 0.39, y, 0.18, 0.17, n, fc=fc, fs=12, bold=True)
    ax.text(0.60, y + 0.085, c, fontsize=11, va="center", color=NERO, linespacing=1.3)
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
righe = [json.loads(r) for r in open("demo/output_esempio/richieste_classificate.jsonl", encoding="utf-8")]
fig, ax = plt.subplots(figsize=(11, 4.4), dpi=200); ax.axis("off")
cols = ["id", "canale", "corso", "tipologia", "urgenza", "operatore", "conf."]
cells = [[r["id"], r["canale"], r["corso"], r["tipologia"], r["urgenza"],
          r["operatore"] if r["assegnazione_automatica"] else "DA VERIFICARE", f"{r['confidenza']:.2f}"] for r in righe]
tab = ax.table(cellText=cells, colLabels=cols, loc="center", cellLoc="left", colLoc="left")
tab.auto_set_font_size(False); tab.set_fontsize(10); tab.scale(1, 1.55)
for (i, j), c in tab.get_celld().items():
    c.set_edgecolor("#D0D0D0")
    if i == 0:
        c.set_facecolor(BORD); c.set_text_props(color="white", fontweight="bold")
    elif cells[i - 1][5] == "DA VERIFICARE":
        c.set_facecolor("#FBE9E7")
    elif cells[i - 1][4] == "alta":
        c.set_facecolor("#FFF4E5")
tab.auto_set_column_width(col=list(range(len(cols))))
salva(fig, "tabella_demo.png")

# 7. quattro passi
fig, ax = fresh(11, 3.6)
passi = [("1. Audit", "canali, volumi,\ntempi (1-2 sett.)"), ("2. Tassonomia\ne dati", "100-200 richieste\netichettate (2 sett.)"),
         ("3. Prototipo", "contenitore, connettori,\nclassificatore (2-4 sett.)"), ("4. Misura\ne decidi", "un mese di metriche,\npoi estendere o fermare")]
for i, (t, d) in enumerate(passi):
    x = 0.02 + i * 0.245
    box(ax, x, 0.50, 0.21, 0.30, t, fc=AZZ if i % 2 == 0 else "#DCE8DC", fs=13, bold=True, tc=BORD)
    ax.text(x + 0.105, 0.42, d, ha="center", va="top", fontsize=10.5, color=NERO, linespacing=1.3)
    if i < 3:
        arrow(ax, x + 0.21, 0.65, x + 0.245, 0.65)
salva(fig, "quattro_passi.png")

# 8. griglia esempio
fig, ax = plt.subplots(figsize=(11, 4.6), dpi=200); ax.axis("off")
cols = ["#", "Passo", "Input", "Decisione", "Tipo"]
cells = [["1", "Raccogliere le richieste", "5 caselle, moduli, Moodle", "nessuna", "Integrazione"],
         ["2", "Estrarre da Zoom e questionari", "chat, risposte aperte", "è una richiesta?", "AI"],
         ["3", "Classificare corso, tipo, urgenza", "testo richiesta", "tassonomia", "AI"],
         ["4", "Assegnare operatore", "tipologia", "competenze per ruolo", "Regola"],
         ["5", "Verificare bassa confidenza", "coda 'da verificare'", "giudizio", "Umano"],
         ["6", "Scrivere la risposta", "richiesta + contesto", "cosa rispondere", "AI"],
         ["7", "Inviare e chiudere", "bozza", "approvazione", "Umano"]]
tab = ax.table(cellText=cells, colLabels=cols, loc="center", cellLoc="left", colLoc="left")
tab.auto_set_font_size(False); tab.set_fontsize(10.5); tab.scale(1, 1.5)
colori = {"AI": "#F6E7D8", "Umano": "#DCE8DC", "Integrazione": AZZ, "Regola": AZZ}
for (i, j), c in tab.get_celld().items():
    c.set_edgecolor("#D0D0D0")
    if i == 0:
        c.set_facecolor(BORD); c.set_text_props(color="white", fontweight="bold")
    elif j == 4:
        c.set_facecolor(colori[cells[i - 1][4]])
tab.auto_set_column_width(col=list(range(len(cols))))
salva(fig, "griglia.png")

# 9. numeri: nessuna figura, si fanno con shape in pptx
print("ok")
