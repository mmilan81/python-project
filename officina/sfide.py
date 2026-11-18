"""Sfide: problemi da risolvere scrivendo il codice, con prove automatiche.

Ogni sfida e' una cartella in missioni/ con "tipo": "sfida" in missione.json.
Il codice del ragazzo viene provato in sottoprocessi isolati: cartella
temporanea, winsound finto (silenzioso) e un limite di tempo. I risultati
attesi restano sul server e non vengono mandati al browser.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path

from errori_it import traduci

BASE = Path(__file__).parent
MISSIONI = BASE / "missioni"
SFIDE = BASE / "progetti" / "sfide"
TIMEOUT = 5

# winsound finto: non suona, registra le note e controlla gli argomenti come quello vero.
WINSOUND_FINTO = '''registro = []

def Beep(frequenza, durata):
    if not isinstance(frequenza, int) or not isinstance(durata, int):
        raise TypeError("'float' object cannot be interpreted as an integer")
    if not 37 <= frequenza <= 32767:
        raise ValueError("frequency must be in 37 thru 32767")
    registro.append((frequenza, durata))
'''

# Prova una singola chiamata di funzione: carica main.py, chiama la funzione, stampa un JSON.
PROVA_FUNZIONE = '''import contextlib, io, json, sys, traceback

spec = json.load(open(sys.argv[1], encoding="utf-8"))
risposta = {}
try:
    with open("main.py", encoding="utf-8") as f:
        sorgente = f.read()
    ns = {"__name__": "modulo"}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(sorgente, "main.py", "exec"), ns)
        nome = spec["f"]
        if not callable(ns.get(nome)):
            risposta["mancante"] = nome
        else:
            import winsound
            winsound.registro.clear()
            risposta["ottenuto"] = ns[nome](*spec["args"])
            risposta["beep"] = [list(b) for b in winsound.registro]
except BaseException:
    risposta["errore"] = traceback.format_exc()
sys.__stdout__.write(json.dumps(risposta, default=repr))
'''


# Lancia main.py con un input() che scrive la domanda su stderr: cosi' lo stdout contiene
# solo cio' che il programma stampa, e si puo' controllare riga per riga.
ESEGUI = r'''import builtins, runpy, sys

def input(prompt=""):
    sys.stderr.write(str(prompt))
    riga = sys.stdin.readline()
    if riga == "":
        raise EOFError("EOF when reading a line")
    return riga.rstrip("\n")

builtins.input = input
runpy.run_path("main.py", run_name="__main__")
'''


def chiave_naturale(nome):
    """s9-... viene prima di s10-..."""
    return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", nome)]


def _env():
    return {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}


def ids_sfide():
    ids = []
    if MISSIONI.exists():
        for p in sorted(MISSIONI.iterdir(), key=lambda q: chiave_naturale(q.name)):
            f = p / "missione.json"
            if p.is_dir() and f.exists():
                try:
                    if json.loads(f.read_text(encoding="utf-8")).get("tipo") == "sfida":
                        ids.append(p.name)
                except ValueError:
                    pass
    return ids


def carica_spec(id_):
    if id_ not in ids_sfide():          # niente percorsi costruiti dal browser
        return None
    return json.loads((MISSIONI / id_ / "missione.json").read_text(encoding="utf-8"))


def file_codice(id_):
    return SFIDE / id_ / "main.py" if id_ in ids_sfide() else None


def titolo_prova(p):
    if p.get("titolo"):
        return p["titolo"]
    args = ", ".join(json.dumps(a, ensure_ascii=False) for a in p.get("args", []))
    return f"{p.get('f', '?')}({args})"


# ---------- confronto dei testi ----------
def normalizza(t):
    t = unicodedata.normalize("NFD", str(t).lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", t).strip()


def _cerca(token, testo):
    """Un numero deve comparire come numero intero (5 non e' dentro 50, ne' dentro 5.5); una parola come testo."""
    t = normalizza(token)
    if re.fullmatch(r"-?\d+([.,]\d+)?", t):
        modello = re.sub(r"\\\.|,", "[.,]", re.escape(t))      # 5.5 e 5,5 sono lo stesso numero
        return re.search(r"(?<![\d.,])" + modello + r"(?!\d)(?![.,]\d)", testo) is not None
    return t in testo


def _spiega_errore(stderr, codice):
    e = traduci(stderr, codice)
    if e is None:
        righe = [r for r in stderr.strip().splitlines() if r.strip()]
        return "Il programma si ferma con un errore: " + (righe[-1] if righe else "sconosciuto")
    dove = f" (riga {e['riga']})" if e["riga"] else ""
    return f"Il programma si ferma con un errore{dove}: {e['spiegazione']}"


def _prova_programma(tmp, prova, codice):
    stdin = "".join(str(x) + "\n" for x in prova.get("input", []))
    try:
        p = subprocess.run([sys.executable, "-u", "_esegui.py"], input=stdin, capture_output=True,
                           text=True, encoding="utf-8", errors="replace",
                           timeout=TIMEOUT, cwd=tmp, env=_env())
    except subprocess.TimeoutExpired:
        return False, "Il programma non finisce entro 5 secondi: c’è un ciclo infinito, oppure aspetta più risposte del previsto."
    if p.returncode != 0:
        return False, _spiega_errore(p.stderr, codice)
    righe = [normalizza(r) for r in p.stdout.splitlines()]
    tutto = normalizza(p.stdout)
    parti = []
    for g in prova.get("righe", []):
        if not any(all(_cerca(t, r) for t in g) for r in righe):
            parti.append("Non trovo una riga che contenga: " + ", ".join(g))
    for t in prova.get("assenti", []):
        if _cerca(t, tutto):
            parti.append("Nel risultato non dovrebbe comparire: " + t)
    if "linee" in prova:      # tutte le righe stampate, nell'ordine, senza righe in piu' o in meno
        attese = [normalizza(x) for x in prova["linee"]]
        ottenute = [normalizza(r) for r in p.stdout.splitlines() if r.strip()]
        if ottenute != attese:
            parti.append("Le righe stampate non sono quelle attese. Mi aspettavo:\n"
                         + "\n".join(prova["linee"][:12]) + (" ..." if len(prova["linee"]) > 12 else ""))
    if not parti:
        return True, None
    parti.append("Il tuo programma ha stampato:\n" + (p.stdout.strip()[:400] or "(niente)"))
    return False, "\n".join(parti)


def _fmt_note(note):
    return ", ".join(f"{f} Hz per {d} ms" for f, d in note) or "nessuna nota"


def _prova_funzione(tmp, prova, codice, indice):
    spec = tmp / f"_spec{indice}.json"
    spec.write_text(json.dumps({"f": prova["f"], "args": prova.get("args", [])}), encoding="utf-8")
    try:
        p = subprocess.run([sys.executable, "-u", "_prova.py", spec.name], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL,
                           timeout=TIMEOUT, cwd=tmp, env=_env())
    except subprocess.TimeoutExpired:
        return False, "La funzione non finisce entro 5 secondi: controlla che nessun ciclo giri all’infinito."
    try:
        r = json.loads(p.stdout.strip().splitlines()[-1])
    except (IndexError, ValueError):
        return False, "Non riesco a leggere il risultato della prova: " + _spiega_errore(p.stderr, codice)
    if r.get("errore"):
        return False, _spiega_errore(r["errore"], codice)
    if r.get("mancante"):
        return False, f"Non trovo una funzione chiamata {r['mancante']}."
    chiamata = titolo_prova(prova)
    if "beep" in prova:
        if r["beep"] == prova["beep"]:
            return True, None
        return False, (f"Chiamata: {chiamata}\nMi aspettavo: {_fmt_note(prova['beep'])}\n"
                       f"Hai suonato: {_fmt_note(r['beep'])}")
    if r["ottenuto"] == prova["atteso"]:
        return True, None
    return False, (f"Chiamata: {chiamata}\nMi aspettavo: {json.dumps(prova['atteso'], ensure_ascii=False)}\n"
                   f"Hai restituito: {json.dumps(r['ottenuto'], ensure_ascii=False)}")


def verifica(spec, codice):
    risultati = []
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        (tmp / "main.py").write_text(codice, encoding="utf-8")
        (tmp / "winsound.py").write_text(WINSOUND_FINTO, encoding="utf-8")
        (tmp / "_esegui.py").write_text(ESEGUI, encoding="utf-8")
        (tmp / "_prova.py").write_text(PROVA_FUNZIONE, encoding="utf-8")
        for i, prova in enumerate(spec.get("prove", [])):
            if "f" in prova:
                ok, dettaglio = _prova_funzione(tmp, prova, codice, i)
            else:
                ok, dettaglio = _prova_programma(tmp, prova, codice)
            nascosta = bool(prova.get("nascosta"))
            risultati.append({
                "titolo": "Prova nascosta" if nascosta else titolo_prova(prova),
                "ok": ok, "extra": bool(prova.get("extra")), "nascosta": nascosta,
                "dettaglio": None if (ok or nascosta) else dettaglio,
            })
    base = [r for r in risultati if not r["extra"]]
    extra = [r for r in risultati if r["extra"]]
    return {"risultati": risultati,
            "ok_base": sum(r["ok"] for r in base), "tot_base": len(base),
            "ok_extra": sum(r["ok"] for r in extra), "tot_extra": len(extra)}


# ---------- storico dei tentativi ----------
def registra(id_, codice, esito):
    cartella = SFIDE / id_
    cartella.mkdir(parents=True, exist_ok=True)
    (cartella / "main.py").write_text(codice, encoding="utf-8")
    riga = {"quando": datetime.now().isoformat(timespec="seconds"),
            **{k: esito[k] for k in ("ok_base", "tot_base", "ok_extra", "tot_extra")}}
    with open(cartella / "tentativi.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(riga) + "\n")


def stato():
    risultato = {}
    for id_ in ids_sfide():
        cartella = SFIDE / id_
        righe = []
        log = cartella / "tentativi.jsonl"
        if log.exists():
            righe = [json.loads(r) for r in log.read_text(encoding="utf-8").splitlines() if r.strip()]
        risultato[id_] = {"tentativi": len(righe), "ultimo": righe[-1] if righe else None,
                          "ha_codice": (cartella / "main.py").exists()}
    return risultato
