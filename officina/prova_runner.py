"""Test automatici del runner (si lanciano con: python prova_runner.py)."""
import json, time
from fastapi.testclient import TestClient
from server import app, PROGETTO

client = TestClient(app, base_url="http://testserver")

def esegui(codice, input_=None, stop_dopo=None):
    with client.websocket_connect("/ws", headers={"origin": "http://testserver"}) as ws:
        ws.send_text(json.dumps({"t": "esegui", "codice": codice}))
        for riga in ([input_] if isinstance(input_, str) else input_ or []):
            time.sleep(0.4); ws.send_text(json.dumps({"t": "stdin", "testo": riga}))
        if stop_dopo:
            time.sleep(stop_dopo); ws.send_text(json.dumps({"t": "stop"}))
        out = ""
        while True:
            m = json.loads(ws.receive_text())
            if m["t"] in ("out", "err"): out += m["testo"]
            else: return out, m["errore"]

o, e = esegui('nome = input("Nome? ")\nprint("Ciao", nome)\n', input_="Luca")
assert "Ciao Luca" in o and e is None, (o, e); print("1 input/output: ok")

o, e = esegui('print(ciao)\n')
assert e["tipo"] == "NameError" and e["riga"] == 1 and "'ciao'" in e["spiegazione"], e; print("2 NameError: ok")

o, e = esegui('if 3 > 2\n    print("si")\n')
assert e["tipo"] == "SyntaxError" and "due punti" in e["suggerimento"].lower() or "Manca" in e["spiegazione"], e; print("3 due punti: ok")

o, e = esegui('print("a" + 5)\n')
assert e["tipo"] == "TypeError" and "str()" in e["suggerimento"], e; print("4 TypeError: ok")

o, e = esegui('x = int("abc")\n')
assert e["tipo"] == "ValueError" and e["riga"] == 1, e; print("5 ValueError: ok")

o, e = esegui('while True:\n    pass\n', stop_dopo=1)
assert e["tipo"] == "stop"; print("6 Stop su ciclo infinito: ok")

o, e = esegui('while True:\n    print("x" * 100)\n')
assert e["tipo"] == "troppo_output"; print("7 limite output: ok")

o, e = esegui('def f():\nprint(1)\n')
assert e["tipo"] == "IndentationError" and "spostata a destra" in e["spiegazione"], e; print("8 indentazione: ok")

try:
    with client.websocket_connect("/ws", headers={"origin": "http://sito-cattivo.example"}) as ws:
        ws.receive_text()
    raise SystemExit("origin esterno accettato!")
except Exception as ex:
    print("9 origin esterno rifiutato: ok")

# ---- missioni ----
lista = [m for m in client.get("/missioni").json() if m.get("tipo") != "sfida"]
assert [m["id"] for m in lista] == ["01-scheda-giocatore", "02-scava-il-diamante", "03-blocco-nota-e-creeper", "04-tavola-da-lavoro", "05-sopravvivenza", "06-blocco-nota-intelligente", "07-tunnel-del-diamante", "08-zaino-e-risorse", "09-jukebox"], lista
assert all(m["partenza"] and m["rotto"] and len(m["passi"]) == 4 for m in lista)
print("10 elenco missioni: ok")

m1, m2, m3, m7, m8, m9 = lista[0], lista[1], lista[2], lista[6], lista[7], lista[8]
o, e = esegui(m1["partenza"], input_=["Steve", "deserto"])
assert e is None and "Steve" in o; print("11 missione 1 partenza: ok")
o, e = esegui(m1["rotto"], input_=["Steve", "200"])
assert e["tipo"] == "TypeError" and e["riga"] == 3, e; print("12 missione 1 rotta, primo errore: ok")
fix = m1["rotto"].replace("blocchi // 64", "int(blocchi) // 64")
o, e = esegui(fix, input_=["Steve", "200"])
assert e["tipo"] == "TypeError" and e["riga"] == 4 and "str()" in e["suggerimento"], e; print("13 missione 1 rotta, secondo errore: ok")
o, e = esegui(m2["partenza"], input_="5")
assert e is None; print("14 missione 2 partenza: ok")
o, e = esegui(m2["rotto"])
assert e["tipo"] == "SyntaxError" and "==" in e["suggerimento"], e; print("15 missione 2 rotta: ok")
assert "range(0, 1000, 100)" in m3["rotto"] and "Beep(440" in m3["partenza"]; print("16 missione 3 file: ok")

# ---- missioni 4-6 ----
(PROGETTO / "random.py").write_text("def randint(a, b):\n    return 40\n", encoding="utf-8")
o, e = esegui(m7["partenza"], input_=["10", "60", "40"])
assert e is None and "Solo terra" in o and "Troppo profondo" in o and "3 tentativi" in o, (o, e); print("17 missione 4 partenza: ok")
o, e = esegui(m7["rotto"], input_="5")
assert e["tipo"] == "NameError" and e["riga"] == 5, e; print("18 missione 4 rotta, primo errore: ok")
fix = m7["rotto"].replace("profondita = 42\n", "profondita = 42\ntentativi = 0\n")
o, e = esegui(fix, input_="5", stop_dopo=2)
assert e["tipo"] in ("stop", "troppo_output"), e; print("19 missione 4 rotta, ciclo infinito fermato: ok")
(PROGETTO / "random.py").unlink()

o, e = esegui(m8["partenza"])
assert e is None and "4 oggetti" in o and "diamanti : 5" in o, (o, e); print("20 missione 5 partenza: ok")
o, e = esegui(m8["rotto"])
assert "Primo oggetto: pala" in o and e["tipo"] == "IndexError" and e["riga"] == 3, (o, e); print("21 missione 5 rotta, IndexError: ok")
o, e = esegui(m8["rotto"].replace("zaino[3]", "zaino[2]"))
assert e["tipo"] == "KeyError" and e["riga"] == 6 and "diamanti" in e["spiegazione"], e; print("22 missione 5 rotta, KeyError: ok")

(PROGETTO / "winsound.py").write_text("def Beep(f, d):\n    print('beep', f, d)\n", encoding="utf-8")
o, e = esegui(m9["partenza"])
assert e is None and o.count("beep") == 7 and "3 stack" in o, (o, e); print("23 missione 6 partenza: ok")
o, e = esegui(m9["rotto"])
assert e["tipo"] == "NameError" and e["riga"] == 6 and "def" in e["suggerimento"], e; print("24 missione 6 rotta, NameError: ok")
fix = m9["rotto"].replace("melodia([262, 294, 330], 300)\n\n", "") + "\nmelodia([262, 294, 330], 300)\n"
o, e = esegui(fix)
assert e["tipo"] == "TypeError" and "durata" in e["messaggio"], e; print("25 missione 6 rotta, TypeError: ok")
fix = fix.replace("suona(frequenza)", "suona(frequenza, durata)")
o, e = esegui(fix)
assert e is None and "None" in o, (o, e); print("26 missione 6 rotta, None silenzioso: ok")
fix = fix.replace("    blocchi // 64", "    return blocchi // 64")
o, e = esegui(fix)
assert e is None and "3 stack" in o, (o, e); print("27 missione 6 riparata: ok")
(PROGETTO / "winsound.py").unlink()

o, e = esegui('z = [1]\nz.remove(5)\n')
assert e["tipo"] == "ValueError" and "lista" in e["spiegazione"], e; print("28 regola remove: ok")
o, e = esegui('z = [1]\nprint(z["a"])\n')
assert e["tipo"] == "TypeError" and "numeri" in e["spiegazione"], e; print("29 regola indice testuale: ok")

# ---- missioni di rinforzo 4-6 ----
n4, n5, n6 = lista[3], lista[4], lista[5]
o, e = esegui(n4["partenza"], input_=["5", "4"])
assert e is None and "Puoi costruire" in o, (o, e)
o, e = esegui(n4["partenza"], input_=["0", "4"])
assert "Ti manca" in o, o
o, e = esegui(n4["partenza"], input_=["0", "1"])
assert "Non hai quasi niente" in o, o; print("30 missione 4 partenza (3 casi): ok")
o, e = esegui(n4["rotto"], input_=["5", "4"])
assert e["tipo"] == "TypeError" and e["riga"] == 6 and "int()" in e["suggerimento"], e; print("31 missione 4 rotta, confronto testo/numero: ok")
fix = n4["rotto"].replace('legno = input("Quanti blocchi di legno hai? ")', 'legno = int(input("Quanti blocchi di legno hai? "))')
o, e = esegui(fix, input_=["0", "4"])
assert e is None and "Non hai quasi niente" in o, (o, e); print("32 missione 4 rotta, bug silenzioso: ok")
fix = fix.replace("elif ferro >= 3 and bastoni >= 2:", "elif ferro >= 3 or bastoni >= 2:")
o, e = esegui(fix, input_=["0", "4"])
assert "Ti manca" in o, o; print("33 missione 4 riparata: ok")

o, e = esegui(n5["partenza"], input_=["8", "si"])
assert e is None and "Vita: 12" in o and "Fame: 16" in o and "così così" in o, (o, e); print("34 missione 5 partenza: ok")
o, e = esegui(n5["rotto"], input_=["8", "si"])
assert e["tipo"] == "SyntaxError" and e["riga"] == 8, e; print("35 missione 5 rotta, due punti: ok")
fix = n5["rotto"].replace('if cibo == "si"\n', 'if cibo == "si":\n')
o, e = esegui(fix, input_=["8", "si"])
assert e["tipo"] == "NameError" and e["riga"] == 5, e; print("36 missione 5 rotta, NameError: ok")
fix = fix.replace("Vita - danno", "vita - danno")
o, e = esegui(fix, input_=["17", "no"])
assert e is None and "così così" in o and "Pericolo" not in o, (o, e); print("37 missione 5 rotta, ordine degli elif: ok")

(PROGETTO / "winsound.py").write_text("def Beep(f, d):\n    if not isinstance(f, int):\n        raise TypeError(\"'float' object cannot be interpreted as an integer\")\n    print('beep', f, d)\n", encoding="utf-8")
o, e = esegui(n6["partenza"], input_=["la", "bassa"])
assert e is None and "a 220 Hz" in o and "beep 220" in o, (o, e)
o, e = esegui(n6["partenza"], input_=["sol#", "normale"])
assert e is None and "Non conosco" in o and "beep" not in o, (o, e); print("38 missione 6 partenza: ok")
o, e = esegui(n6["rotto"], input_=["si", "normale"])
assert e["tipo"] == "NameError" and "frequenza" in e["spiegazione"], e; print("39 missione 6 rotta, NameError: ok")
fix = n6["rotto"].replace('nota == "Si"', 'nota == "si"')
o, e = esegui(fix, input_=["la", "bassa"])
assert e["tipo"] == "TypeError" and "intero" in e["spiegazione"], (o, e); print("40 missione 6 rotta, float: ok")
fix = fix.replace("frequenza / 2", "frequenza // 2")
o, e = esegui(fix, input_=["la", "bassa"])
assert e is None and "beep 220" in o, (o, e); print("41 missione 6 riparata: ok")
(PROGETTO / "winsound.py").unlink()

# ---- sfide ----
import json as _j
import sfide as _sfide
tutte = client.get("/missioni").json()
sf = [m for m in tutte if m.get("tipo") == "sfida"]
assert [m["id"] for m in sf] == ["s1-commerciante", "s2-minatore", "s3-registro-zaino", "s4-scala-musicale", "s5-paghetta", "s6-gioco-del-buzz", "s7-ora-di-arrivo", "s8-media-dei-voti", "s9-resto-al-bar", "s10-numeri-primi"], [m["id"] for m in sf]
blob = _j.dumps(tutte)
assert "prove" not in sf[0] and '"atteso"' not in blob and '"righe"' not in blob and '"beep"' not in blob
assert all(m["modello"] and m["prove_pubbliche"] and m["prove_nascoste"] >= 1 for m in sf)
print("42 sfide elencate, senza risultati attesi: ok")

def verifica(id_, codice):
    r = client.post("/verifica", json={"id": id_, "codice": codice}, headers={"origin": "http://testserver"})
    assert r.status_code == 200, r.text
    return r.json()

SOL = {
"s1-commerciante": """smeraldi = int(input("Quanti smeraldi hai? "))
prezzo = int(input("Quanto costa un oggetto? "))
if prezzo <= 0:
    print("Prezzo non valido")
elif smeraldi < prezzo:
    print("Non hai abbastanza smeraldi")
else:
    print("Puoi comprare", smeraldi // prezzo, "oggetti")
    print("Ti avanzano", smeraldi % prezzo, "smeraldi")
""",
"s2-minatore": """n = int(input("Quanti livelli vuoi scavare? "))
if n < 0:
    print("Numero non valido")
else:
    totale = 0
    for livello in range(1, n + 1):
        blocchi = livello * 3
        print("Livello", str(livello) + ":", blocchi)
        totale = totale + blocchi
    print("Totale:", totale)
""",
"s3-registro-zaino": """def conta_oggetti(zaino):
    conteggio = {}
    for oggetto in zaino:
        conteggio[oggetto] = conteggio.get(oggetto, 0) + 1
    return conteggio

def piu_frequente(zaino):
    conteggio = conta_oggetti(zaino)
    migliore = None
    for nome in conteggio:
        if migliore is None or conteggio[nome] > conteggio[migliore]:
            migliore = nome
    return migliore

print(conta_oggetti(["a", "a"]))
""",
"s4-scala-musicale": """import winsound

def scala(partenza, passo, quante):
    for i in range(quante):
        winsound.Beep(partenza + i * passo, 200)

def scala_discendente(partenza, passo, quante):
    for i in range(quante):
        winsound.Beep(partenza - i * passo, 200)

scala(262, 50, 3)
""",
}
for id_, codice in SOL.items():
    d = verifica(id_, codice)
    assert d["ok_base"] == d["tot_base"] and d["ok_extra"] == d["tot_extra"], (id_, d)
print("43 soluzioni corrette: tutte le prove passano (4 sfide): ok")

for m in sf:
    d = verifica(m["id"], m["modello"])
    assert d["ok_base"] < d["tot_base"], (m["id"], d)
print("44 i modelli vuoti non passano: ok")

# soluzione sbagliata: off-by-one nel range
sbagliata = SOL["s2-minatore"].replace("range(1, n + 1)", "range(1, n)")
d = verifica("s2-minatore", sbagliata)
visibili_ko = [r for r in d["risultati"] if not r["ok"] and not r["nascosta"]]
assert d["ok_base"] < d["tot_base"] and any("Non trovo una riga" in (r["dettaglio"] or "") for r in visibili_ko), d
assert all(r["dettaglio"] is None for r in d["risultati"] if r["nascosta"])
print("45 off-by-one: bocciato, con spiegazione e prove nascoste senza dettagli: ok")

# risposta scritta a mano (hardcoded): passa la prima prova ma non le altre
fissa = 'input()\ninput()\nprint("Puoi comprare 5 oggetti")\nprint("Ti avanzano 2 smeraldi")\n'
d = verifica("s1-commerciante", fissa)
assert d["risultati"][0]["ok"] and d["ok_base"] < d["tot_base"], d
print("46 risposta scritta a mano: smascherata: ok")

d = verifica("s3-registro-zaino", "def conta_oggetti(zaino):\n    return list(zaino)\n")
assert any("Hai restituito" in (r["dettaglio"] or "") for r in d["risultati"]), d
d = verifica("s4-scala-musicale", SOL["s4-scala-musicale"].replace("range(quante)", "range(1, quante + 1)"))
assert any("Hai suonato" in (r["dettaglio"] or "") for r in d["risultati"]), d
d = verifica("s3-registro-zaino", "x = 1\n")
assert any("Non trovo una funzione" in (r["dettaglio"] or "") for r in d["risultati"]), d
print("47 funzioni sbagliate o mancanti: dettagli chiari: ok")

d = verifica("s1-commerciante", "print(ciao)\n")
assert any("(riga 1)" in (r["dettaglio"] or "") and "ciao" in (r["dettaglio"] or "") for r in d["risultati"]), d
d = verifica("s3-registro-zaino", "x = input()\n")
assert any("input" in (r["dettaglio"] or "").lower() for r in d["risultati"]), d
print("48 errori tradotti nelle prove: ok")

_sfide.TIMEOUT = 1
d = verifica("s1-commerciante", "while True:\n    pass\n")
_sfide.TIMEOUT = 5
assert d["ok_base"] == 0 and any("non finisce" in (r["dettaglio"] or "") for r in d["risultati"]), d
print("49 ciclo infinito fermato: ok")

d = verifica("s1-commerciante", SOL["s1-commerciante"])
r = client.get("/sfide/stato").json()
assert r["s1-commerciante"]["tentativi"] >= 5 and r["s1-commerciante"]["ultimo"]["ok_base"] == 5 and r["s1-commerciante"]["ha_codice"], r
assert client.get("/sfide/s1-commerciante/codice").json()["codice"] == SOL["s1-commerciante"]
print("50 storico e codice salvato: ok")

assert client.post("/verifica", json={"id": "s1-commerciante", "codice": ""}, headers={"origin": "http://sito-cattivo.example"}).status_code == 403
assert client.post("/verifica", json={"id": "01-scheda-giocatore", "codice": ""}, headers={"origin": "http://testserver"}).status_code == 404
assert client.post("/verifica", json={"id": "../prova", "codice": ""}, headers={"origin": "http://testserver"}).status_code == 404
assert client.get("/sfide/..%2Fprova/codice").status_code == 404
assert client.get("/sfide/01-scheda-giocatore/codice").status_code == 404
print("51 origine esterna e id non validi rifiutati: ok")

# ---- sfide su numeri e vita di tutti i giorni (5-10) ----
assert all(m.get("gruppo") for m in sf)
assert {m["gruppo"] for m in sf} == {"Sfide con Minecraft e musica", "Sfide con numeri e vita di tutti i giorni"}
NUOVE = {
"s5-paghetta": """prezzo = int(input("Quanto costa il gioco? "))
risparmi = int(input("Quanti euro hai già? "))
paghetta = int(input("Quanto ricevi ogni settimana? "))
if risparmi >= prezzo:
    print("Puoi già comprarlo")
elif paghetta <= 0:
    print("Con questa paghetta non ci riuscirai mai")
else:
    mancano = prezzo - risparmi
    settimane = mancano // paghetta
    if mancano % paghetta != 0:
        settimane = settimane + 1
    print("Servono", settimane, "settimane")
""",
"s6-gioco-del-buzz": """n = int(input("Fino a che numero conto? "))
if n < 1:
    print("Niente da contare")
for i in range(1, n + 1):
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
""",
"s7-ora-di-arrivo": """def ora_di_arrivo(ore, minuti, durata):
    totale = ore * 60 + minuti + durata
    totale = totale % 1440
    return [totale // 60, totale % 60]

def formatta_ora(ore, minuti):
    o = str(ore)
    m = str(minuti)
    if ore < 10:
        o = "0" + o
    if minuti < 10:
        m = "0" + m
    return o + ":" + m
""",
"s8-media-dei-voti": """totale = 0
quanti = 0
voto = int(input("Voto (0 per finire): "))
while voto != 0:
    if voto >= 1 and voto <= 10:
        totale = totale + voto
        quanti = quanti + 1
    else:
        print("Voto non valido")
    voto = int(input("Voto (0 per finire): "))
if quanti == 0:
    print("Nessun voto inserito")
else:
    media = totale / quanti
    print("Media:", media)
    if media >= 6:
        print("Promosso")
    else:
        print("Non promosso")
""",
"s9-resto-al-bar": """def monete_di_resto(centesimi):
    tagli = [200, 100, 50, 20, 10, 5, 2, 1]
    monete = []
    for taglio in tagli:
        while centesimi >= taglio:
            monete.append(taglio)
            centesimi = centesimi - taglio
    return monete

def resto_da_pagare(prezzo, pagato):
    if pagato < prezzo:
        return None
    return monete_di_resto(pagato - prezzo)
""",
"s10-numeri-primi": """def e_primo(n):
    if n < 2:
        return False
    for divisore in range(2, n):
        if n % divisore == 0:
            return False
    return True

def primi_fino_a(n):
    primi = []
    for k in range(2, n + 1):
        if e_primo(k):
            primi.append(k)
    return primi
""",
}
for id_, codice in NUOVE.items():
    d = verifica(id_, codice)
    assert d["ok_base"] == d["tot_base"] and d["ok_extra"] == d["tot_extra"], (id_, d)
print("52 sfide 5-10: le soluzioni di riferimento passano tutte le prove: ok")

for m in sf[4:]:
    d = verifica(m["id"], m["modello"])
    assert d["ok_base"] < d["tot_base"], (m["id"], d)
print("53 sfide 5-10: i modelli vuoti non passano: ok")

SBAGLIATE = {
 "s5-paghetta": NUOVE["s5-paghetta"].replace("    if mancano % paghetta != 0:\n        settimane = settimane + 1\n", ""),
 "s6-gioco-del-buzz": NUOVE["s6-gioco-del-buzz"].replace("i % 15 == 0", "i % 3 == 0 and i % 5 == 0 and False"),
 "s7-ora-di-arrivo": NUOVE["s7-ora-di-arrivo"].replace("totale % 1440", "totale"),
 "s8-media-dei-voti": NUOVE["s8-media-dei-voti"].replace("totale / quanti", "totale // quanti"),
 "s9-resto-al-bar": NUOVE["s9-resto-al-bar"].replace("while centesimi >= taglio:", "if centesimi >= taglio:"),
 "s10-numeri-primi": NUOVE["s10-numeri-primi"].replace("    if n < 2:\n        return False\n", ""),
}
for id_, codice in SBAGLIATE.items():
    d = verifica(id_, codice)
    assert d["ok_base"] < d["tot_base"], (id_, d)
    assert any(r["dettaglio"] for r in d["risultati"] if not r["ok"] and not r["nascosta"]), (id_, d)
print("54 errori tipici (arrotondamento, ordine, mezzanotte, //, if al posto di while, caso 1): bocciati: ok")

d = verifica("s7-ora-di-arrivo", "def ora_di_arrivo(ore, minuti, durata):\n    return [15, 15]\n")
assert d["risultati"][0]["ok"] and d["ok_base"] < d["tot_base"], d
d = verifica("s6-gioco-del-buzz", "n = int(input())\nfor i in range(1, n + 1):\n    print(i)\n")
assert any("Mi aspettavo" in (r["dettaglio"] or "") for r in d["risultati"]), d
d = verifica("s6-gioco-del-buzz", 'n = int(input("Fino a che numero conto? "))\nprint("Conto fino a", n)\nfor i in range(1, n + 1):\n    print(i)\n')
assert d["ok_base"] == 0, d
print("55 risposta scritta a mano e righe esatte: ok")

# la domanda di input() non deve sporcare le righe stampate
d = verifica("s6-gioco-del-buzz", NUOVE["s6-gioco-del-buzz"].replace('input("Fino a che numero conto? ")', 'input("Fino a che numero conto? ")'))
assert d["ok_base"] == d["tot_base"]
print("56 le domande di input() non sporcano l'output controllato: ok")
