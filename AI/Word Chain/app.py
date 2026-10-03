import os
import secrets
import time
from collections import defaultdict, deque

import numpy as np
from flask import Flask, jsonify, render_template, request
from gensim.models import KeyedVectors

MODEL_FILE = os.environ.get("MODEL_FILE", "challenge_filtered.model")
HINT_KEY = os.environ.get("HINT_KEY", "a4dw-wd31-wwe32-dd24")
FLAG = os.environ.get("FLAG", "d4rk{pr0bability_1s_A_f03}")
THRESHOLD = 0.30
NODE = "__node_7f3a__"

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024

# Load the model once at process startup. No user-controlled path is accepted.
model = KeyedVectors.load(MODEL_FILE, mmap="r")
vocabulary = set(model.key_to_index)
start_words = [w for w in vocabulary if w != NODE]

# Small in-memory rate limiter. For a multi-worker deployment, put nginx/Caddy
# in front as well; this limiter is intentionally process-local.
WINDOW = 60.0
MAX_REQUESTS = 90
requests_by_ip = defaultdict(deque)

def client_ip():
    # Do not trust X-Forwarded-For unless your reverse proxy is configured to
    # sanitize it. Docker's direct connection address is safe for this use.
    return request.remote_addr or "unknown"

def rate_limited():
    now = time.monotonic()
    q = requests_by_ip[client_ip()]
    while q and now - q[0] > WINDOW:
        q.popleft()
    if len(q) >= MAX_REQUESTS:
        return True
    q.append(now)
    return False

def json_error(message, status=400):
    return jsonify({"ok": False, "error": message}), status

@app.after_request
def security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self'; script-src 'self'; "
        "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; "
        "base-uri 'none'; form-action 'self'"
    )
    response.headers["Cache-Control"] = "no-store"
    return response

@app.get("/")
def index():
    return render_template("index.html", threshold=int(THRESHOLD * 100))

@app.post("/api/start")
def start():
    if rate_limited():
        return json_error("Too many requests. Slow down.", 429)
    if not start_words:
        return json_error("No valid starting words are available.", 500)
    current = secrets.choice(start_words)
    return jsonify({"ok": True, "current": current, "threshold": THRESHOLD})

@app.post("/api/step")
def step():
    data = request.get_json(silent=True) or {}

    current = data.get("current", "").strip().lower()
    word = data.get("word", "").strip().lower()

    if not current or not word:
        return jsonify({"error": "Missing word"}), 400

    if current not in model.key_to_index:
        return jsonify({"error": "Invalid current word"}), 400

    if word not in model.key_to_index:
        return jsonify({
            "accepted": False,
            "similarity": 0,
            "message": "That word isn't in the vocabulary."
        }), 400

    similarity = float(model.similarity(current, word))
    percentage = similarity * 100

    accepted = similarity >= THRESHOLD

    if not accepted:
        return jsonify({
            "accepted": False,
            "similarity": percentage,
            "message": f"Rejected. Need at least {THRESHOLD * 100:.0f}% similarity."
        })

    won = word == "__node_7f3a__"

    return jsonify({
        "accepted": True,
        "similarity": percentage,
        "current": word,
        "won": won,
        "flag": FLAG if won else None,
        "message": "Accepted."
    })

@app.post("/api/similar")
def similar():
    if rate_limited():
        return json_error("Too many requests. Slow down.", 429)

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return json_error("Invalid JSON.")

    word = data.get("word")
    hint = data.get("hint")

    if not isinstance(word, str) or not isinstance(hint, str):
        return json_error("Invalid request.")
    word = word.strip().lower()

    # Do not expose the similarity map unless the exact hint key is supplied.
    if not secrets.compare_digest(hint, HINT_KEY):
        return json_error("Invalid hint key.", 403)
    if word not in vocabulary:
        return json_error("Word isn't in the vocabulary.")

    limit = 10
    results = model.most_similar(word, topn=limit)
    return jsonify({
        "ok": True,
        "results": [
            {"word": w, "similarity": round(float(score), 6), "percentage": round(float(score) * 100, 2)}
            for w, score in results
        ]
    })

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "model_loaded": True})

if __name__ == "__main__":
    # Production container uses gunicorn; this is only a local fallback.
    app.run(host="0.0.0.0", port=5066)
