import sys
import asyncio
import uvicorn

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

if __name__ == "__main__":
    # HOST 0.0.0.0 permette a Docker di "esporre" il sito all'esterno
    uvicorn.run("server:app", host="0.0.0.0", port=8000)