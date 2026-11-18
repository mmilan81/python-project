"""Officina: runner Python locale per imparare a programmare.

Avvio:  uvicorn server:app --host 127.0.0.1 --port 8000
Il codice scritto nell'editor gira con il Python vero, in un sottoprocesso,
dentro la cartella progetti/prova (quindi file, pip e librerie funzionano).
"""
import asyncio
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

from fastapi import Body, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

import sfide
from errori_it import MOTIVI, traduci

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

BASE = Path(__file__).parent

BASE = Path(__file__).parent
PROGETTO = BASE / "progetti" / "prova"
PROGETTO.mkdir(parents=True, exist_ok=True)
MISSIONI = BASE / "missioni"

TIMEOUT_SECONDI = 120      # rete di sicurezza; il ragazzo ha comunque Stop
MAX_OUTPUT = 200_000       # caratteri: ferma i print in ciclo infinito

app = FastAPI()


@app.get("/")
def indice():
    return FileResponse(BASE / "static" / "index.html")


@app.get("/missioni")
def elenco_missioni():
    """Legge le cartelle in missioni/ (in ordine di nome) e le restituisce al pannello."""
    risultato = []
    if not MISSIONI.exists():
        return risultato
    for cartella in sorted((p for p in MISSIONI.iterdir() if p.is_dir()), key=lambda q: sfide.chiave_naturale(q.name)):
        meta_file = cartella / "missione.json"
        if not meta_file.exists():
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        meta["id"] = cartella.name
        for nome in ("partenza", "rotto", "modello"):
            f = cartella / f"{nome}.py"
            meta[nome] = f.read_text(encoding="utf-8") if f.exists() else None
        if meta.get("tipo") == "sfida":
            # le prove (con i risultati attesi) restano sul server: al browser solo i titoli
            prove = meta.pop("prove", [])
            meta["prove_pubbliche"] = [{"titolo": sfide.titolo_prova(p), "extra": bool(p.get("extra"))}
                                       for p in prove if not p.get("nascosta")]
            meta["prove_nascoste"] = sum(1 for p in prove if p.get("nascosta"))
        risultato.append(meta)
    return risultato


def solo_stessa_origine(request: Request):
    origin = request.headers.get("origin")
    if origin and urlparse(origin).netloc != request.headers.get("host"):
        raise HTTPException(status_code=403, detail="origine non consentita")


@app.post("/verifica")
def verifica(request: Request, dati: dict = Body(...)):
    solo_stessa_origine(request)
    codice = dati.get("codice", "")
    if not isinstance(codice, str) or len(codice) > 100_000:
        raise HTTPException(status_code=400, detail="codice non valido")
    spec = sfide.carica_spec(dati.get("id"))
    if spec is None:
        raise HTTPException(status_code=404, detail="sfida non trovata")
    esito = sfide.verifica(spec, codice)
    sfide.registra(dati["id"], codice, esito)
    return esito


@app.get("/sfide/stato")
def stato_sfide():
    return sfide.stato()


@app.get("/sfide/{id_sfida}/codice")
def codice_sfida(id_sfida: str):
    f = sfide.file_codice(id_sfida)
    if f is None:
        raise HTTPException(status_code=404, detail="sfida non trovata")
    return {"codice": f.read_text(encoding="utf-8") if f.exists() else ""}


@app.get("/codice")
def codice_salvato():
    f = PROGETTO / "main.py"
    return {"codice": f.read_text(encoding="utf-8") if f.exists() else ""}


async def svuota(*flussi):
    """Dopo un kill legge e scarta quello che resta nelle pipe, cosi' il processo si chiude davvero."""
    async def uno(f):
        while await f.read(65536):
            pass
    try:
        await asyncio.wait_for(asyncio.gather(*(uno(f) for f in flussi)), 5)
    except asyncio.TimeoutError:
        pass


async def supervisiona(ws, proc, codice, stato):
    """Legge stdout/stderr del processo, li inoltra al browser e applica i limiti."""
    err_buffer = []
    totale = {"n": 0}

    async def leggi(stream, canale):
        while True:
            dati = await stream.read(1024)
            if not dati:
                return
            testo = dati.decode("utf-8", "replace")
            if canale == "err":
                err_buffer.append(testo)
            totale["n"] += len(testo)
            if totale["n"] > MAX_OUTPUT:
                if not stato.get("motivo"):
                    stato["motivo"] = "troppo_output"
                    proc.kill()
                continue  # scarta il testo ma continua a svuotare la pipe, altrimenti wait() si blocca
            await ws.send_text(json.dumps({"t": canale, "testo": testo}))

    try:
        await asyncio.wait_for(
            asyncio.gather(leggi(proc.stdout, "out"), leggi(proc.stderr, "err"), proc.wait()),
            TIMEOUT_SECONDI,
        )
    except asyncio.TimeoutError:
        stato["motivo"] = "timeout"
        proc.kill()
        await svuota(proc.stdout, proc.stderr)
    await proc.wait()

    motivo = stato.get("motivo")
    if motivo:
        sp, sug = MOTIVI[motivo]
        errore = {"tipo": motivo, "spiegazione": sp, "suggerimento": sug, "riga": None, "testo_riga": None}
    else:
        errore = traduci("".join(err_buffer), codice)
    try:
        await ws.send_text(json.dumps({"t": "fine", "codice": proc.returncode, "errore": errore}))
    except Exception:
        pass


@app.websocket("/ws")
async def ws_endpoint(ws: WebSocket):
    # Difesa: una pagina web qualsiasi non deve poter far eseguire codice sul PC.
    origin = ws.headers.get("origin")
    if origin and urlparse(origin).netloc != ws.headers.get("host"):
        await ws.close(code=1008)
        return
    await ws.accept()

    proc = None
    task = None
    stato = {}
    try:
        while True:
            msg = json.loads(await ws.receive_text())
            tipo = msg.get("t")

            if tipo == "esegui" and (proc is None or proc.returncode is not None):
                codice = msg.get("codice", "")
                (PROGETTO / "main.py").write_text(codice, encoding="utf-8")
                stato = {}
                env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
                proc = await asyncio.create_subprocess_exec(
                    sys.executable, "-u", "main.py",
                    cwd=PROGETTO, env=env,
                    stdin=asyncio.subprocess.PIPE,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                task = asyncio.create_task(supervisiona(ws, proc, codice, stato))

            elif tipo == "stdin" and proc and proc.returncode is None:
                try:
                    # Modifica cruciale per Windows: usiamo \r\n e togliamo il drain() che causa blocchi
                    proc.stdin.write((msg.get("testo", "") + "\r\n").encode("utf-8"))
                except Exception:
                    pass

            elif tipo == "stop" and proc and proc.returncode is None:
                stato["motivo"] = "stop"
                proc.kill()
    except WebSocketDisconnect:
        pass
    finally:
        if proc and proc.returncode is None:
            proc.kill()
