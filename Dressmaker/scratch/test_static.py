import urllib.request
import threading
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.backend.server import run_server

server = run_server(port=7898)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()
time.sleep(0.5)

try:
    for route in ["/", "/styles.css", "/app.js"]:
        url = f"http://127.0.0.1:7898{route}"
        with urllib.request.urlopen(url) as res:
            content = res.read()
            mime = res.headers.get("Content-Type")
            print(f"Rota {route} -> Código {res.status}, Mime: {mime}, Tamanho: {len(content)} bytes")
finally:
    server.shutdown()
