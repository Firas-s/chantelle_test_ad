import base64
import os

from pathlib import Path
import sys
path_root = Path(__file__).parents[0]
sys.path.append(str(path_root))

from src import main
from src import init
from flask import Flask, request


app = Flask(__name__)
@app.route("/cl", methods=["POST"])
def cl():
    min = request.args.get('min')
    max = request.args.get('max')
    return (main.ingest(min, max,"cl"), 200)

@app.route("/dj", methods=["POST"])
def dj():
    min = request.args.get('min')
    max = request.args.get('max')
    return (main.ingest(min, max,"dj"), 200)

@app.route("/init_dj", methods=["POST"])
def djinit():
    min = request.args.get('min')
    max = request.args.get('max')
    return (init.ingest("2022-10-01", "2023-03-01","dj"), 200)

@app.route("/init_cl", methods=["POST"])
def clinit():
    min = request.args.get('min')
    max = request.args.get('max')
    return (init.ingest("2022-01-01", "2023-03-01","cl"), 200)

if __name__ == "__main__":
    PORT = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    app.run(host="127.0.0.1", port=PORT, debug=True)