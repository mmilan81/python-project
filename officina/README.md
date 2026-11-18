# Officina

App locale per imparare Python scrivendo codice vero.

## Avvio

    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn server:app --host 127.0.0.1 --port 8000

Poi apri http://127.0.0.1:8000. Esegui = Ctrl+Invio.

Le missioni sono nella cartella `missioni/` (vedi `missioni/LEGGIMI.md`) e compaiono
nel pannello a sinistra. Dopo aver aggiunto o cambiato file riavvia il server.

Il libricino (teoria, esempi pratici e progetti) e' in `dispensa/`: `dispensa-python.html` si apre nel browser
e si stampa (Ctrl+P), `dispensa-python.md` e' lo stesso testo in Markdown.

Le Sfide (in fondo al pannello) chiedono di scrivere il codice da zero: il pulsante Controlla lo prova
con casi diversi e salva ogni tentativo in `progetti/sfide/` (vedi `missioni/LEGGIMI.md`).

Il codice viene salvato in `progetti/prova/main.py` a ogni esecuzione.

## Test

    python prova_runner.py   # serve: pip install httpx

## Sicurezza

Il server esegue codice arbitrario: lascialo su 127.0.0.1 (mai 0.0.0.0) e non
esporlo su internet. Le connessioni da pagine di altri siti sono rifiutate.


Per far partire il progetto:
nella cartella python_project
python -m venv .venv
poi entra nella cartella officina
.venv\Scripts\activate
uvicorn server:app --reload