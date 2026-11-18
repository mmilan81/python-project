# Missioni

Ogni cartella e' una missione, con tre file:

- `missione.json`: titolo, concetti e i quattro passi (prevedi, modifica, ripara, spiega)
- `partenza.py`: il codice che il pulsante "Prova" carica nell'editor
- `rotto.py`: la versione con i bug, caricata da "Carica versione da riparare"

Per aggiungere una missione crea una nuova cartella (es. `04-nome`) con gli stessi
tre file. Compare da sola nel pannello dopo il riavvio del server.

Per chi fa da copilota: non dare le risposte. Chiedi "cosa pensi che succeda?" e
lascia sbagliare. Se e' bloccato da piu' di 5 minuti, indica dove guardare
(la riga segnalata nel riquadro), mai la soluzione.

## Sfide

Una sfida e' una cartella con `"tipo": "sfida"` in `missione.json` e un `modello.py`
(il file di partenza, con lo spazio per il PIANO). Le prove stanno in `prove`:

- programma che legge input: `{"input": [47, 9], "righe": [["5"], ["2"]], "assenti": ["..."]}`.
  Ogni gruppo in `righe` e' una riga dell'output che deve contenere tutti quei pezzi
  (i numeri devono comparire interi: 5 non e' dentro 50; maiuscole e accenti non contano).
- funzione: `{"f": "nome", "args": [...], "atteso": ...}`, oppure `"beep": [[Hz, ms], ...]`
  per controllare le note suonate con winsound (durante le prove winsound e' finto e silenzioso).
- `"extra": true` per le prove facoltative, `"nascosta": true` per quelle di cui il ragazzo
  vede solo l'esito: servono a scoprire se la soluzione funziona davvero o se e' scritta
  su misura per gli esempi.

I risultati attesi restano sul server e non arrivano al browser.

### Per chi fa da copilota: vedere come lavora

Ogni volta che preme "Controlla", il codice viene salvato in `progetti/sfide/<id-sfida>/`:

- `main.py`: l'ultimo codice controllato. In cima c'e' il PIANO: leggilo, e' li' che si vede come ragiona.
- `tentativi.jsonl`: una riga per tentativo, con la data e le prove superate.

Quanti tentativi ha fatto, se ha scritto il piano prima del codice, se i casi particolari
li ha pensati lui o li ha scoperti dalle prove: sono tutti indizi su come organizza il pensiero.
Non dare la soluzione: chiedigli "cosa si aspettava la prova e cosa hai ottenuto tu?".
