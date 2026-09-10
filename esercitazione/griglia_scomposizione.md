# Griglia di scomposizione di un processo

Prima di parlare di agenti, si scompone il processo. Compilate una riga per
ogni passo. Un passo per riga, anche se sembra banale.

La lezione e' da remoto: questa griglia si compila da soli, non in gruppo.
Dieci minuti, poi ne scomponiamo una insieme dal vivo. Copiatela in un foglio
di calcolo, in un documento, o su carta: l'importante e' che sia vostra.

| # | Passo | Chi lo fa oggi | Input (da dove arriva) | Decisione (sì/no, quale regola) | Output (dove finisce) | AI, integrazione o umano? |
|---|-------|----------------|------------------------|----------------------------------|-----------------------|----------------------------|
| 1 |       |                |                        |                                  |                       |                            |
| 2 |       |                |                        |                                  |                       |                            |
| 3 |       |                |                        |                                  |                       |                            |
| 4 |       |                |                        |                                  |                       |                            |
| 5 |       |                |                        |                                  |                       |                            |

## Come riempire l'ultima colonna

- **Integrazione**: spostare dati da un posto a un altro senza interpretarli
  (da 5 caselle a una; da un modulo a una tabella). Non serve AI.
- **AI**: leggere testo non strutturato e produrre un campo strutturato
  (classificare, estrarre, riassumere, abbozzare). Serve un modello.
- **Umano**: decisioni con responsabilità o con informazione che il sistema
  non ha (inviare, promettere una data, gestire un reclamo, casi ambigui).
- Se la regola si scrive in un "se... allora", è integrazione, non AI.

## Tre domande finali (una riga a testa, in chat)

1. Qual è il passo che, automatizzato, fa risparmiare più tempo?
2. Qual è il passo dove un errore del sistema costa di più?
3. Quale numero misurereste dopo un mese per decidere se continuare?

## Esempio compilato: helpdesk formazione (esigenza 3)

| # | Passo | Chi | Input | Decisione | Output | Tipo |
|---|-------|-----|-------|-----------|--------|------|
| 1 | Raccogliere le richieste | Segreteria | 5 caselle, moduli sito, Moodle | nessuna | Tabella unica | Integrazione |
| 2 | Estrarre richieste da Zoom e questionari | nessuno oggi | chat, risposte aperte | è una richiesta? | Righe in tabella | AI |
| 3 | Classificare corso, tipo, urgenza | Segreteria | testo richiesta | tassonomia | 4 campi | AI |
| 4 | Assegnare operatore | Segreteria | tipo | competenze per ruolo | operatore | Integrazione (regola) |
| 5 | Verificare i casi a bassa confidenza | Segreteria | coda "da verificare" | giudizio | campi corretti | Umano |
| 6 | Scrivere la risposta | Operatore | richiesta + contesto | cosa rispondere | bozza | AI |
| 7 | Inviare e chiudere | Operatore | bozza | approvazione | risposta inviata, stato chiusa | Umano |
