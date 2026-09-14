"""Rigenera prompt_unico.md da istruzioni.md e da data/tassonomia.yaml.

Il prompt unico e' il ripiego per quando non si fa in tempo a creare il GPT
personalizzato: stesse istruzioni, ma la tassonomia va dentro il messaggio
invece che in un file allegato. Va rigenerato quando la tassonomia cambia.

    python demo/gpt_personalizzato/genera_prompt_unico.py
"""
from pathlib import Path

RADICE = Path(__file__).resolve().parents[2]
istruzioni = (RADICE / "demo/gpt_personalizzato/istruzioni.md").read_text(encoding="utf-8")
corpo = istruzioni[istruzioni.index("Sei il sistema di smistamento"):
                   istruzioni.index("non l'helpdesk.") + len("non l'helpdesk.")]
tassonomia = (RADICE / "data/tassonomia.yaml").read_text(encoding="utf-8").strip()
uscita = RADICE / "demo/gpt_personalizzato/prompt_unico.md"
testo = uscita.read_text(encoding="utf-8")
testa = testo[:testo.index("---\n\n") + 5]
uscita.write_text(f"{testa}\n{corpo}\n\nQuesta \u00e8 la tassonomia da usare. \u00c8 l'unica fonte "
                  f"delle categorie ammesse:\nnon inventarne altre, non tradurle, non accorparle."
                  f"\n\n```yaml\n{tassonomia}\n```\n\nQuando hai letto tutto, rispondi solo: "
                  f'"Pronto. Mandami le richieste."\n\n---\n', encoding="utf-8")
print(f"rigenerato {uscita}")
