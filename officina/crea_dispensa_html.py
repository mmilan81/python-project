"""Rigenera dispensa/dispensa-python.html da dispensa/dispensa-python.md.

Uso:  pip install markdown   e poi   python crea_dispensa_html.py
"""
from pathlib import Path

import markdown

CSS = """
:root { color-scheme: light dark; --testo:#1d2733; --sfondo:#ffffff; --codice:#f0f3f7; --bordo:#d5dce5; --accento:#0b7a63; }
@media (prefers-color-scheme: dark) { :root { --testo:#e4e8ee; --sfondo:#12161d; --codice:#1c232d; --bordo:#2d3744; --accento:#5fd3b8; } }
body { margin: 0; background: var(--sfondo); color: var(--testo); font: 17px/1.6 "Atkinson Hyperlegible", system-ui, "Segoe UI", sans-serif; }
main { max-width: 46rem; margin: 0 auto; padding: 2rem 1.25rem 4rem; }
h1 { font-size: 2rem; margin: 0 0 .25rem; }
h2 { font-size: 1.4rem; margin: 2.5rem 0 .5rem; padding-top: .75rem; border-top: 2px solid var(--bordo); color: var(--accento); }
h3 { font-size: 1.15rem; margin: 1.75rem 0 .4rem; }
h4 { font-size: 1rem; margin: 1.25rem 0 .3rem; }
code, pre { font-family: "JetBrains Mono", ui-monospace, Consolas, Menlo, monospace; font-size: .9em; }
code { background: var(--codice); padding: .1em .35em; border-radius: 4px; }
pre { background: var(--codice); border: 1px solid var(--bordo); border-radius: 6px; padding: .8rem 1rem; overflow-x: auto; line-height: 1.45; }
pre code { background: none; padding: 0; }
li { margin: .25rem 0; }
@media print {
  :root { --testo:#000; --sfondo:#fff; --codice:#f4f4f4; --bordo:#bbb; --accento:#000; }
  body { font-size: 11pt; } main { max-width: none; padding: 0; }
  h2 { break-after: avoid; } pre { break-inside: avoid; white-space: pre-wrap; }
}
"""

base = Path(__file__).parent / "dispensa"
corpo = markdown.markdown((base / "dispensa-python.md").read_text(encoding="utf-8"),
                          extensions=["fenced_code", "sane_lists"])
html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dispensa di Python: le basi</title>
<style>{CSS}</style>
</head>
<body><main>
{corpo}
</main></body>
</html>
"""
(base / "dispensa-python.html").write_text(html, encoding="utf-8")
print("dispensa-python.html aggiornata")
