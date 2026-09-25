import urllib.request
import json
import threading
import time
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.backend.server import run_server

server = run_server(port=7899)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()
time.sleep(0.5)

try:
    with urllib.request.urlopen("http://127.0.0.1:7899/api/status") as res:
        data = json.loads(res.read().decode('utf-8'))
        print("Status retornado pela API:")
        print(data)
finally:
    server.shutdown()
    print("Servidor de teste encerrado com sucesso.")
