"""Traduce gli errori di Python in spiegazioni comprensibili per un ragazzo.

Idea: il traceback originale resta SEMPRE visibile (e' quello che vedra' sul
lavoro). Qui aggiungiamo accanto una spiegazione in italiano e un suggerimento.
"""
import re

# (tipo errore, regex sul messaggio) -> (spiegazione, suggerimento)
# Le regole sono provate in ordine: la prima che combacia vince.
REGOLE = [
    ("IndentationError", r"expected an indented block",
     "Dopo una riga che finisce con i due punti ( : ) la riga successiva deve essere spostata a destra.",
     "Premi Tab all'inizio della riga che segue if, for, while o def."),
    ("IndentationError", r"unexpected indent",
     "Questa riga e' spostata a destra senza motivo.",
     "Il rientro serve solo dopo i due punti. Togli gli spazi in piu' all'inizio della riga."),
    ("IndentationError", r"unindent does not match",
     "Il rientro di questa riga non combacia con nessuna delle righe sopra.",
     "Controlla di usare lo stesso numero di spazi per tutte le righe dello stesso blocco."),
    ("SyntaxError", r"expected ':'",
     "Manca il simbolo : alla fine della riga.",
     "if, elif, else, for, while, def e class vogliono sempre i due punti in fondo."),
    ("SyntaxError", r"'(\W)' was never closed",
     "Hai aperto una parentesi che non hai mai chiuso.",
     "Conta le parentesi della riga indicata (e di quella sopra): ogni ( vuole il suo )."),
    ("SyntaxError", r"unmatched '(\W)'",
     "C'e' una parentesi chiusa che non corrisponde a nessuna aperta.",
     "Controlla di non averne scritta una di troppo."),
    ("SyntaxError", r"unterminated string literal",
     "Hai aperto un testo con le virgolette ma non l'hai chiuso.",
     "Il testo deve iniziare e finire con lo stesso tipo di virgolette."),
    ("SyntaxError", r"Missing parentheses in call to 'print'",
     "In Python 3 print si scrive con le parentesi.",
     "Scrivi print(\"ciao\") invece di print \"ciao\"."),
    ("SyntaxError", r"Maybe you meant '==' or ':='",
     "Qui serve un confronto, ma hai usato un solo =.",
     "= assegna un valore, == confronta due valori. Dentro un if di solito vuoi =="),
    ("SyntaxError", r"invalid syntax",
     "Python non riesce a leggere questa riga: qualcosa e' scritto in modo non valido.",
     "Guarda la riga indicata e anche quella subito sopra: spesso manca una virgola, una parentesi o dei due punti."),
    ("NameError", r"name '(.+)' is not defined",
     "Python non sa cosa sia '{0}'.",
     "Controlla: l'hai scritto uguale (maiuscole comprese)? Hai creato la variabile PRIMA di usarla? Se e' un testo, servono le virgolette. Se e' una funzione, la riga def deve stare PRIMA della riga che la chiama."),
    ("UnboundLocalError", r"local variable '(.+)'",
     "Stai usando '{0}' dentro una funzione prima di averle dato un valore.",
     "Dai un valore alla variabile prima di leggerla."),
    ("TypeError", r"can only concatenate str \(not \"(\w+)\"\) to str",
     "Stai unendo un testo con un valore di tipo {0}, e Python non lo fa da solo.",
     "Trasforma il numero in testo con str(), oppure usa una f-string: f\"Ho {{eta}} anni\"."),
    ("TypeError", r"not supported between instances of '(\w+)' and '(\w+)'",
     "Stai confrontando un valore di tipo {0} con uno di tipo {1}, e Python non sa dire quale sia il maggiore.",
     "Ricorda che input() restituisce testo: trasformalo con int() prima di confrontarlo con un numero."),
    ("TypeError", r"'float' object cannot be interpreted as an integer",
     "Questa funzione vuole un numero intero, ma ha ricevuto un decimale (per esempio 220.0).",
     "La divisione con / restituisce sempre un decimale. Usa // per avere un intero, oppure int()."),
    ("TypeError", r"unsupported operand type",
     "Stai facendo un'operazione tra due tipi di dati che non si possono combinare (per esempio testo e numero).",
     "input() restituisce sempre testo: se ti serve un numero usa int() o float()."),
    ("TypeError", r"missing (\d+) required positional argument",
     "Hai chiamato una funzione senza dare tutti i valori che richiede.",
     "Guarda dove la funzione e' definita (def): conta quanti parametri ha."),
    ("TypeError", r"takes (\d+) positional arguments? but (\d+) (?:was|were) given",
     "Hai dato alla funzione un numero sbagliato di valori.",
     "Confronta la chiamata con la riga def della funzione."),
    ("TypeError", r"'(\w+)' object is not callable",
     "Stai usando come funzione qualcosa che non lo e' (tipo {0}).",
     "Succede spesso quando una variabile ha lo stesso nome di una funzione, o manca un operatore prima di una parentesi."),
    ("TypeError", r"list indices must be integers",
     "Le posizioni di una lista sono numeri, non testi.",
     "Per trovare un valore dal suo nome serve un dizionario. In una lista si usa la posizione: zaino[0]."),
    ("TypeError", r"object is not subscriptable|not iterable",
     "Stai usando [ ] o un ciclo su qualcosa che non e' una lista, un testo o un dizionario.",
     "Stampa la variabile con print() e controlla che tipo di valore contiene."),
    ("ValueError", r"invalid literal for int\(\) with base 10: (.+)",
     "Hai provato a trasformare {0} in un numero intero, ma non e' un numero.",
     "Controlla cosa ha scritto l'utente: spazi, lettere o virgole decimali (in Python si usa il punto)."),
    ("ValueError", r"not in list",
     "Stai togliendo dalla lista qualcosa che non c'e'.",
     "Controlla come e' scritto l'elemento, oppure verifica prima con: if elemento in lista."),
    ("ValueError", r"could not convert string to float: (.+)",
     "Hai provato a trasformare {0} in un numero decimale, ma non lo e'.",
     "I decimali si scrivono con il punto: 3.5 e non 3,5."),
    ("ZeroDivisionError", r"",
     "Hai provato a dividere per zero, e in matematica non si puo'.",
     "Controlla con un if che il divisore non sia 0 prima di dividere."),
    ("IndexError", r"list index out of range|string index out of range",
     "Hai chiesto una posizione che non esiste.",
     "Le posizioni partono da 0: una lista di 3 elementi ha le posizioni 0, 1, 2. Controlla con len()."),
    ("KeyError", r"(.+)",
     "Nel dizionario non c'e' la chiave {0}.",
     "Controlla come l'hai scritta, oppure usa dizionario.get(chiave) che non da' errore."),
    ("AttributeError", r"'(\w+)' object has no attribute '(\w+)'",
     "Un valore di tipo {0} non ha niente che si chiami '{1}'.",
     "Controlla il nome (una lettera sbagliata e' un classico) e il tipo del valore con type()."),
    ("FileNotFoundError", r"No such file or directory: (.+)",
     "Il file {0} non esiste, almeno non nella cartella dove gira il programma.",
     "Controlla il nome e l'estensione, e che il file sia nella cartella del progetto."),
    ("ModuleNotFoundError", r"No module named '(.+)'",
     "Python non trova il modulo '{0}'.",
     "Controlla il nome. Se e' una libreria esterna va installata con: pip install {0}"),
    ("RecursionError", r"",
     "Una funzione continua a richiamare se stessa senza mai fermarsi.",
     "Serve una condizione di uscita, cioe' un caso in cui la funzione NON si richiama."),
    ("EOFError", r"",
     "Il programma ha chiesto un input ma non ne ha ricevuto.",
     "Scrivi la risposta nella riga sotto l'output e premi Invio."),
]

MOTIVI = {
    "timeout": ("Il programma e' stato fermato: girava da troppo tempo.",
                "Probabile ciclo infinito: controlla che la condizione del while diventi falsa prima o poi."),
    "troppo_output": ("Il programma e' stato fermato: stava scrivendo troppo testo.",
                      "Probabile ciclo infinito con un print dentro."),
    "stop": ("Hai fermato il programma.", ""),
}


def _ultima_riga_errore(stderr):
    for riga in reversed(stderr.strip().splitlines()):
        if re.match(r"^[A-Za-z_][\w.]*(Error|Exception|Interrupt|Exit)\b", riga):
            return riga
    return None


def _riga_del_codice(stderr):
    trovate = re.findall(r'File "[^"]*main\.py", line (\d+)', stderr)
    return int(trovate[-1]) if trovate else None


def traduci(stderr, codice):
    """Ritorna un dict con la spiegazione, oppure None se non c'e' nessun errore."""
    if not stderr.strip():
        return None
    riga_err = _ultima_riga_errore(stderr)
    if riga_err is None:
        return None
    tipo, _, messaggio = riga_err.partition(":")
    tipo, messaggio = tipo.strip(), messaggio.strip()
    n = _riga_del_codice(stderr)
    righe = codice.splitlines()
    testo_riga = righe[n - 1].strip() if n and n <= len(righe) else None

    spiegazione = suggerimento = None
    for t, pattern, sp, sug in REGOLE:
        if t != tipo:
            continue
        m = re.search(pattern, messaggio)
        if m:
            spiegazione, suggerimento = sp.format(*m.groups()), sug.format(*m.groups())
            break
    if spiegazione is None:
        spiegazione = f"Python ha segnalato un errore di tipo {tipo}."
        suggerimento = "Leggi l'ultima riga dell'errore: di solito dice cosa non va. Poi guarda la riga indicata."
    return {"tipo": tipo, "messaggio": messaggio, "riga": n, "testo_riga": testo_riga,
            "spiegazione": spiegazione, "suggerimento": suggerimento}
